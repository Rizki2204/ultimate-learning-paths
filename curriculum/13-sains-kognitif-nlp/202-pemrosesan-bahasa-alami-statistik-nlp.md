# Modul 202: Pemrosesan Bahasa Alami Statistik / NLP (Model Bahasa N-Gram, Tokenisasi BPE/WordPiece, Word2Vec, GloVe, CRF)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 13: Tingkat 13: Sains Kognitif, Neuroengineering & Computational Linguistics](./README.md)
*Sebelumnya*: [201. linguistik-formal-komputasional](./201-linguistik-formal-komputasional.md) | *Berikutnya*: [203. arsitektur-transformer-mekanisme-atensi](./203-arsitektur-transformer-mekanisme-atensi.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana komputer bisa mengerti kata-kata manusia? Bagi komputer, sebuah kata hanyalah deretan karakter biner tanpa jiwa. Jika Anda merepresentasikan kata sebagai angka ID alfabet biasa (misal: "Kucing" = 1, "Anjing" = 2, "Pesawat" = 3), komputer tidak tahu bahwa kucing dan anjing memiliki banyak kesamaan (keduanya hewan berkaki empat berbulu), sedangkan pesawat adalah mesin terbang ([Mikolov et al. - Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781)).

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Linguis J. R. Firth (1957) merumuskan hipotesis terkenal: *"You shall know a word by the company it keeps"* (Anda akan mengenali arti suatu kata dari teman-teman kata yang sering muncul di sampingnya) ([Firth - A Synopsis of Linguistic Theory 1930-1955](https://www.jstor.org/stable/410886)).

Inilah fondasi **Word Embedding (seperti Word2Vec dan GloVe)**: memetakan setiap kata menjadi panah vektor dalam ruang geometri berdimensi 300 ([Pennington et al. - GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf)). Dalam ruang ini, kata-kata yang bermakna mirip akan mengelompok bersama secara otomatis, dan yang menakjubkan, kita bisa melakukan perhitungan aljabar matematika pada makna konsep kata:
$$\vec{v}_{\text{Raja}} - \vec{v}_{\text{Pria}} + \vec{v}_{\text{Wanita}} \approx \vec{v}_{\text{Ratu}}$$
Sebelum kata bisa dipetakan ke vektor, teks harus dipotong menjadi sub-kata menggunakan algoritma **Byte Pair Encoding (BPE)** agar komputer tidak pernah bingung saat menghadapi kata baru yang belum pernah dilihat sebelumnya ([Sennrich et al. - Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Matematis NLP Statistik & Representasi Vektor:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
1. **Pemodelan Bahasa N-Gram & Smoothing Kneser-Ney**:
Probabilitas sekuens kata di bawah asumsi rantai Markov orde $(n-1)$:
$$P(w_1, \dots, w_T) = \prod_{t=1}^T P(w_t \mid w_{t-n+1}, \dots, w_{t-1})$$
Kneser-Ney Smoothing menyisipkan probabilitas kelanjutan (*continuation probability*) $P_{KN}$:
$$P_{KN}(w_i \mid w_{i-1}) = \frac{\max(C(w_{i-1}, w_i) - d, 0)}{C(w_{i-1})} + \lambda(w_{i-1}) \frac{|\{w' : C(w', w_i) > 0\}|}{\sum_{w} |\{w' : C(w', w) > 0\}|}$$

2. **Algoritma Tokenisasi Byte Pair Encoding (BPE)**:
Dimulai dari kosakata karakter dasar. Secara iteratif menghitung pasangan byte/simbol berdekatan yang memiliki frekuensi kemunculan tertinggi $p^* = \arg\max_p \text{Count}(p)$ dan menggabungkannya (*merge*) menjadi satu token baru hingga mencapai ukuran kosakata target $V$ ([Gage - A New Algorithm for Data Compression](https://www.drdobbs.com/a-new-algorithm-for-data-compression/184402829)).

3. **Word2Vec Skip-Gram dengan Negative Sampling (SGNS)**:
Memaksimalkan probabilitas kata konteks $w_c$ diberikan kata target $w_t$ sambil meminimalkan probabilitas $k$ kata derau acak $w_{n_j} \sim P_n(w)$ ([Mikolov et al. NeurIPS 2013](https://arxiv.org/abs/1310.4546)):
$$\mathcal{L}_{\text{SGNS}} = \sum_{t=1}^T \sum_{-c \le j \le c, j \neq 0} \left[ \ln \sigma(v'_{w_{t+j}}^T v_{w_t}) + \sum_{i=1}^k \mathbb{E}_{w_{n_i} \sim P_n(w)} \left[ \ln \sigma(-v'_{w_{n_i}}^T v_{w_t}) \right] \right]$$

4. **Global Vectors for Word Representation (GloVe)**:
Memfaktorkan matriks ko-okurensi logaritmik global $X_{ij}$:
$$J = \sum_{i, j=1}^V f(X_{ij}) \left( w_i^T \tilde{w}_j + b_i + \tilde{b}_j - \ln X_{ij} \right)^2, \quad f(x) = \min\left(1, \left(\frac{x}{x_{\max}}\right)^\alpha\right)$$

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur pipeline tokenisasi BPE dan komputasi embedding Skip-Gram Word2Vec:

```mermaid
flowchart LR
    RawText["Raw Text: 'pembelajaran mendalam'"] --> BPE["BPE Subword Tokenizer (HuggingFace tokenizers)"]
    BPE --> Tokens["Token IDs: [1845, 934, 12044]"]
    Tokens --> EmbeddingTable["Embedding Lookup Matrix E in R^(V x D)"]
    EmbeddingTable --> DenseVec["Dense Dense Continuous Vector in R^D (D=768)"]
```

Dengan tokenisasi sub-kata BPE, representasi kosakata tertutup rapat: kata-kata langka atau typo didekonstruksi menjadi potongan suku kata dasar tanpa pernah menghasilkan token *Out-Of-Vocabulary (OOV)* ([Sennrich et al. BPE Paper](https://arxiv.org/abs/1508.07909)).

#### Tabel Penelusuran Ruang Vektor Word2Vec & Proyeksi Subruang Bias Gender
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Ingest Corpus Berita Besar | Korpus Google News (3 Juta Kata) | Pelatihan Model Word2Vec Skip-Gram | Matriks embedding $W \in \mathbb{R}^{3M \times 300}$ | Model memetakan kemunculan bersama kata | Ruang vektor semantik 300 dimensi terbentuk |
| 2. Identifikasi Vektor Arah Gender | Pasangan Kata Biner: Pria - Wanita | Vektor selisih: $\mathbf{g} = \mathbf{v}(\text{"he"}) - \mathbf{v}(\text{"she"})$ | Dekomposisi PCA pada pasangan gender | Komponen utama ke-1 mendefinisikan sumbu gender | Sumbu $\mathbf{g}$ memotong ruang semantik |
| 3. Aritmatika Vektor Bias Naif | Analogi: $\mathbf{v}(\text{"man"}) : \mathbf{v}(\text{"programmer"}) = \mathbf{v}(\text{"woman"}) : \mathbf{x}$ | $\mathbf{x} \approx \mathbf{v}(\text{"programmer"}) - \mathbf{v}(\text{"man"}) + \mathbf{v}(\text{"woman"})$ | Matriks tetangga terdekat Cosine Similarity | Kata terdekat: $\mathbf{x} \to \text{"homemaker"}$ | Model mereproduksi stereotipe gender budaya masa lalu |
| 4. Deteksi Token Glitch BPE | Token Anomali: `"SolidGoldMagikarp"` | Algoritma Tokenisasi Byte-Pair Encoding | Token muncul di korpus reddit tanpa konteks wajar | Vektor embedding terisolasi di sudut ekstrem ruang laten | LLM menghasilkan halusinasi toksik saat token dipanggil |
| 5. Mitigasi Hard Debiasing Bolukbasi | Proyeksi Ortogonal Subruang Netral | $\mathbf{w}_{\text{debiased}} = \mathbf{w} - (\mathbf{w} \cdot \mathbf{g}) \mathbf{g}$ | Netralisasi kata pekerjaan (programmer, doctor, nurse) | Sumbu gender diisolasi murni ke kata biologis (ibu, ayah) | Representasi semantik adil, seimbang, dan bebas bias asosiasi |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import collections

# 1. Implementasi Algoritma Byte Pair Encoding (BPE) Mini dari Nol
def train_bpe(corpus, num_merges=10):
    # Inisialisasi korpus menjadi karakter terpisah dengan simbol akhir kata '</w>'
    vocab = collections.defaultdict(int)
    for word, freq in corpus.items():
        tokens = " ".join(list(word)) + " </w>"
        vocab[tokens] = freq
        
    merges = []
    for step in range(num_merges):
        pairs = collections.defaultdict(int)
        for word_str, freq in vocab.items():
            symbols = word_str.split()
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i+1])] += freq
                
        if not pairs:
            break
            
        best_pair = max(pairs, key=pairs.get)
        merges.append(best_pair)
        
        # Gabungkan pasangan terbaik di seluruh kosakata
        new_vocab = {}
        bigram = " ".join(best_pair)
        replacement = "".join(best_pair)
        for word_str, freq in vocab.items():
            new_word = word_str.replace(bigram, replacement)
            new_vocab[new_word] = freq
        vocab = new_vocab
        
    return merges, vocab

# Korpus Contoh Teks Bahasa Indonesia
raw_corpus = {"kucing": 5, "kucingku": 3, "anjing": 4, "anjingku": 2, "kucingan": 1}
bpe_merges, final_vocab = train_bpe(raw_corpus, num_merges=6)

print("Aturan Penggabungan BPE (Merges Teratas):")
for idx, pair in enumerate(bpe_merges, start=1):
    print(f"Merge #{idx}: {pair[0]} + {pair[1]} -> {''.join(pair)}")

print("\nKosakata Akhir Terbina:")
for tokenized_word in final_vocab.keys():
    print(f" - {tokenized_word}")
```

## 5. Miskonsepsi & Jebakan Industri
*Ambiguitas Polisemi pada Static Word Embeddings*: Model seperti Word2Vec atau GloVe menetapkan tepat satu vektor statis untuk setiap kata. Kata seperti "bisa" (racun ular vs mampu melakukan sesuatu) atau "apel" (buah vs upacara militer) dipaksa berbagi satu titik koordinat yang sama, mencampuradukkan makna semantiknya. Keterbatasan inilah yang memicu lahirnya *Contextual Word Embeddings* (BERT, GPT, dan Transformers) di mana representasi vektor kata berubah secara dinamis sesuai konteks kalimatnya ([Peters et al. - Deep Contextualized Word Representations / ELMo](https://arxiv.org/abs/1802.05365)).

### Studi Kasus Kegagalan Nyata: Skandal Bias Stereotipe Gender Word2Vec & Kerentanan Glitch Token BPE (2016/2023)
- **Kronologi & Konteks Sejarah**: Pada tahun 2016, penelitian penting oleh Tolga Bolukbasi dkk. (Boston University & Microsoft Research) mengungkap bahwa model representasi kata paling populer di dunia saat itu, Google Word2Vec, memuat bias stereotipe gender yang sangat diskriminatif. Ketika diuji dengan operasi aritmatika vektor semantik (*"Man is to Computer Programmer as Woman is to X"*), model tersebut secara konsisten menjawab *"Homemaker"* (ibu rumah tangga), serta memetakan profesi medis seperti *"Doctor"* ke pria dan *"Nurse"* ke wanita.
- **Akar Masalah Representasi Vektor Kata & Algoritma Tokenisasi**: Model Word2Vec Skip-Gram dan GloVe dilatih untuk memprediksi kata berdasarkan konteks kemunculan bersamanya dalam miliaran kata berita publik. Model tidak memiliki filter moral atau pemahaman sosiologis; model memproyeksikan prasangka historis teks masyarakat secara langsung ke dalam ruang geometri Euclidean. Sumbu arah gender (*gender subspace*) secara tidak sengaja mengkontaminasi kata-kata profesi netral. Fenomena kerapuhan representasi serupa terulang pada era LLM modern dalam bentuk **BPE Glitch Tokens** (2023): algoritma tokenisasi Byte-Pair Encoding menghasilkan token anomali (seperti `SolidGoldMagikarp` atau `StreamerBot`) yang sering muncul dalam dataset pengelompokan token namun jarang muncul saat pra-pelatihan model, menghasilkan vektor bobot yang tidak teratur (*untrained weights*) yang memicu respons halusinasi liar atau pengulangan kata kutukan saat pengguna memasukkan token tersebut.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```python
# Analisis Bias Geometri Vektor Semantik: Proyeksi Subruang vs Netralisasi Ortogonal
import numpy as np

# SIMULASI BIAS WORD2VEC: Menghitung proyeksi kata profesi terhadap sumbu gender
def check_gender_bias_projection(word_vector, gender_direction_vector):
    # gender_direction_vector: normalisasi dari v("he") - v("she")
    g = gender_direction_vector / np.linalg.norm(gender_direction_vector)
    
    # Skalar proyeksi: Seberapa jauh kata profesi tertarik ke arah gender maskulin/feminin
    bias_score = np.dot(word_vector, g)
    return bias_score # Pada model lama: "programmer" bernilai +0.45 (Maskulin)!

# MITIGASI HARD DEBIASING (Bolukbasi et al., 2016)
def neutralize_word_embedding(word_vector, gender_direction_vector):
    g = gender_direction_vector / np.linalg.norm(gender_direction_vector)
    
    # Mengeliminasi komponen vektor yang sejajar dengan sumbu gender (Proyeksi Ortogonal)
    projection = np.dot(word_vector, g) * g
    debiased_vector = word_vector - projection
    
    # Normalisasikan kembali vektor hasil:
    debiased_vector = debiased_vector / np.linalg.norm(debiased_vector)
    return debiased_vector # Kini ortogonal murni terhadap bias gender (bias_score = 0.0)!
```

- **Analisis Forensik & Rekayasa Modern**: Krisis bias representasi dan glitch token menghasilkan standar rekayasa NLP modern: (1) Penerapan algoritma **Hard Debiasing & Soft Debiasing** pada tahap pra-pemrosesan matriks embedding; (2) Pemeriksaan kebersihan kamus tokenisasi (*Vocabulary Pruning & Glitch Token Auditing*) sebelum pra-pelatihan dimulai untuk menghapus token anomali yang tidak memiliki representasi representatif; (3) Integrasi evaluasi penanda bias otomatis (**WEAT: Word Embedding Association Test**) dalam pipeline integrasi berkelanjutan (CI/CD) model bahasa.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Bangun model bahasa Bi-Gram dan Tri-Gram sederhana dengan Laplace Add-1 Smoothing di Python, dan hitung nilai perplexity model pada kalimat uji baru.
*Rubrik*: Perplexity terhitung secara matematis $PP(W) = \exp\left(-\frac{1}{N}\sum \ln P(w_i \mid w_{i-1})\right)$.

### Level 2 (Menengah)
Implementasikan arsitektur Continuous Bag-of-Words (CBOW) Word2Vec sederhana di PyTorch: rancang lapisan embedding input dan output, latih menggunakan Negative Sampling loss pada korpus teks mini, dan buktikan kata-kata yang sering muncul bersamaan memiliki nilai kemiripan kosinus (*Cosine Similarity*) $> 0.7$.
*Rubrik*: Menghasilkan matriks embedding berdimensi 50 dan fungsi pencarian k-tetangga terdekat.

### Level 3 (Mahir)
Implementasikan algoritma penandaan urutan *Linear-Chain Conditional Random Field (CRF)* untuk Named Entity Recognition (NER) dari awal: turunkan algoritma Forward-Backward untuk menghitung fungsi partisi normalisasi $Z(x)$, implementasikan Viterbi decoding untuk inferensi urutan label optimal, dan bandingkan performa terhadap model klasifikasi independen token.
*Rubrik*: Mengeliminasi prediksi transisi status yang tidak valid (misal: token `I-PER` tanpa diawali `B-PER`).

### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma tokenisasi Byte-Pair Encoding (BPE) sederhana dari nol dalam Python: Buat fungsi yang menerima korpus teks pendek, memecah kata menjadi karakter individual dengan penanda akhir kata `</w>`, menghitung pasangan byte/simbol yang paling sering muncul (*Most Frequent Bigram Pair*), dan secara berulang menggabungkan pasangan tersebut selama 10 iterasi penggabungan (*merge operations*).
- **Petunjuk Perancangan Arsitektur**:
  - Simpan frekuensi kata dalam dictionary: `{'l o w </w>': 5, 'l o w e s t </w>': 2, ...}`.
  - Cari bigram dengan frekuensi kemunculan tertinggi pada seluruh korpus.
  - Ganti seluruh kemunculan pasangan tersebut dengan token gabungan baru.
- **Test Vector & Kasus Uji**:
  - Korpus: `"low low low low low lowest lowest newer newer newer newer wider wider"`.
  - Pasangan frekuensi tertinggi pertama: `('e', 'r')` -> digabung menjadi `'er'`.
  - Tampilkan daftar 10 aturan penggabungan (*Merge Rules*) yang dihasilkan secara urut.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma BPE presisi, kalkulasi frekuensi bigram benar, aturan merge tersimpan konsisten.
  - Skor 50%: BPE bekerja namun salah menangani penanda akhir kata `</w>` sehingga mencampurkan batas antar kata.
  - Skor 0%: Menggunakan pemotongan string biasa tanpa kalkulasi pasangan terpopuler.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul pengujian bias semantik Word Embedding Association Test (WEAT) dari nol dalam Python menggunakan NumPy: Hitung ukuran efek (*Effect Size* $d$) dan signifikansi statistik p-value permutasi untuk menguji hipotesis asosiasi antara dua himpunan kata target (misal: Karier vs Keluarga) terhadap dua himpunan kata atribut (misal: Pria vs Wanita).
- **Petunjuk Perancangan Arsitektur**:
  - Cosine similarity: $s(w, A, B) = \text{mean}_{a \in A} \cos(w, a) - \text{mean}_{b \in B} \cos(w, b)$.
  - Statistik uji diferensial: $S(X, Y, A, B) = \sum_{x \in X} s(x, A, B) - \sum_{y \in Y} s(y, A, B)$.
  - Effect Size $d = \frac{\text{mean}_{x \in X} s(x, A, B) - \text{mean}_{y \in Y} s(y, A, B)}{\text{std}_{w \in X \cup Y} s(w, A, B)}$.
  - Lakukan 1.000 uji permutasi acak untuk menghitung nilai p-value non-parametrik.
- **Test Vector & Kasus Uji**:
  - Berikan matriks embedding sintetis yang memuat bias terstruktur (kata karier memiliki cosine similarity lebih tinggi ke atribut pria).
  - Modul WEAT harus melaporkan effect size positif yang signifikan ($d > 1.2, p < 0.01$).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi WEAT presisi, uji permutasi acak tepat, kalkulasi effect size Cohen's d akurat.
  - Skor 50%: Menghitung skor asosiasi benar namun salah mengkalkulasi standar deviasi gabungan pada pembagi.
  - Skor 0%: Mengasumsikan uji-t parametrik biasa tanpa uji permutasi non-parametrik.

### Tingkat 3: Mahir
- **Tugas**: Rancang pipeline sanitasi kosakata tokenisasi (*Token Vocabulary Auditor & Glitch Token Scanner*) dalam Python: Bangun alat diagnostik otomatis yang menerima model bahasa yang sudah dilatih (atau representasi embedding-nya) dan memindai seluruh 50.000 token dalam tokenizer untuk mendeteksi token anomalik yang memiliki: (1) Norma gradien tidak normal; (2) Jarak Euclidean ekstrem dari centroid ruang embedding; (3) Kegagalan decoding round-trip (`decode(encode(token)) != token`).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung distribusi norma vektor embedding: $r_i = \|v_i\|_2$. Identifikasi token pencilan di atas persentil 99.9%.
  - Lakukan kueri deteksi k-Nearest Neighbors: token glitch biasanya tidak memiliki tetangga terdekat yang memiliki relasi semantik wajar.
  - Hasilkan dokumen rekomendasi karantina token (*Quarantine Manifest*) yang dapat di-load oleh runtime inferensi untuk memblokir token berbahaya.
- **Test Vector & Kasus Uji**:
  - Injeksi 5 token anomali buatan dengan norma ekstrem atau string byte tak terdefinisi ke dalam vocab.
  - Scanner harus mendeteksi ke-5 token anomali tersebut secara tepat dengan tingkat false positive $< 0.1\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pipeline deteksi anomali multi-dimensi presisi, penanganan edge-case karakter Unicode byte rapi.
  - Skor 50%: Deteksi bekerja hanya berdasarkan panjang string tanpa menganalisis sifat geometri vektor embedding.
  - Skor 0%: Hanya mengecek round-trip string tanpa inspeksi representasi laten.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Efficient Estimation of Word Representations in Vector Space (Word2Vec) | Tomas Mikolov et al. (Google) | [arXiv Word2Vec Paper](https://arxiv.org/abs/1301.3781) | Algoritma Skip-Gram, Continuous Bag-of-Words, Neg-Sampling |
| GloVe: Global Vectors for Word Representation | Jeffrey Pennington, Richard Socher, Christopher D. Manning | [Stanford NLP Paper](https://nlp.stanford.edu/pubs/glove.pdf) | Faktorisasi Matriks Ko-Okurensi Logaritmik Global |
| Neural Machine Translation of Rare Words with Subword Units (BPE) | Rico Sennrich, Barry Haddow, Alexandra Birch | [arXiv BPE Paper](https://arxiv.org/abs/1508.07909) | Standar Baku Industri Tokenisasi Sub-Kata pada LLM |
| Speech and Language Processing (Chapter 6: Vector Semantics) | Dan Jurafsky & James H. Martin | [Jurafsky SLP3 Chapter 6](https://web.stanford.edu/~jurafsky/slp3/6.pdf) | Teori Semantik Vektor, Cosine Similarity, Evaluasi Analogi |

---
*Navigasi Cepat*: [Ke Tingkat 13](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [201. linguistik-formal-komputasional](./201-linguistik-formal-komputasional.md) | *Berikutnya*: [203. arsitektur-transformer-mekanisme-atensi](./203-arsitektur-transformer-mekanisme-atensi.md)
