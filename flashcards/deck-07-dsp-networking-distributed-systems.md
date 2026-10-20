# Tingkat 8, 9 & 10: Pemrosesan Sinyal, Jaringan Komputer & Sistem Terdistribusi

**Deck ID**: `deck-07-dsp-networking-distributed-systems`  
**Jumlah Kartu**: 25 kartu active recall  
**Tingkat Kurikulum Terkait**:
- Tingkat 8: [08-dsp-telekomunikasi-jaringan](../curriculum/08-dsp-telekomunikasi-jaringan/README.md)
- Tingkat 9: [09-software-engineering-cloud-sre](../curriculum/09-software-engineering-cloud-sre/README.md)
- Tingkat 10: [10-basis-data-enterprise](../curriculum/10-basis-data-enterprise/README.md)

## Deskripsi & Ruang Lingkup Pengetahuan
Penguasaan teorema Nyquist, FFT, stack TCP/IP, algoritma kongesti BBR/Cubic, CAP/PACELC theorem, konsensus Raft/Paxos, dan LSM-Tree database storage.

## Petunjuk Penggunaan
1. **Format Anki TSV**: Berkas pendamping `.tsv` siap diimpor langsung ke Anki dengan tipe catatan *Cloze* (pemisah Tab).
2. **Studi Mandiri Markdown**: Anda dapat mempelajari kartu di bawah secara langsung. Bagian dalam kurung tebal `**[Kunci Jawaban]**` merepresentasikan kata kunci yang diuji.

## Daftar Ringkasan Kartu
| No | Kategori | Ringkasan Pertanyaan | Tags |
|---|---|---|---|
| 01 | Foundational Definitions | Teorema Sampling Nyquist-Shannon menyatakan bahwa agar sinyal waktu-kontinu dengan frek... | `tier-08::dsp` |
| 02 | Mathematical Identities | Persamaan Transformasi Fourier Diskrit (Discrete Fourier Transform - DFT) untuk sinyal ... | `tier-08::dsp` |
| 03 | Mathematical Identities | Algoritma Fast Fourier Transform (FFT) Cooley-Tukey memangkas kompleksitas komputasi tr... | `tier-08::dsp` |
| 04 | Mathematical Identities | Kapasitas kanal transmisi maksimum teoritis C dalam bit per detik pada kanal transmisi ... | `tier-08::telekomunikasi` |
| 05 | Architecture Constants | Ukuran unit transmisi maksimum standar (Maximum Transmission Unit - MTU) pada jaringan ... | `tier-08::networking` |
| 06 | Architecture Constants | Ukuran minimum header paket IPv4 standar tanpa opsi tambahan adalah **[20 byte]**, dan ... | `tier-08::networking` |
| 07 | Foundational Definitions | Tiga langkah jabat tangan pembentukan koneksi TCP (Three-Way Handshake) secara beruruta... | `tier-08::networking` |
| 08 | Architecture Constants | Status penutupan koneksi TCP di mana inisiator penutupan wajib menunggu selama durasi 2... | `tier-08::networking` |
| 09 | Mathematical Identities | Algoritma kontrol kongesti TCP CUBIC memodelkan pertumbuhan jendela kongesti (cwnd) seb... | `tier-08::networking` |
| 10 | Foundational Definitions | Dua fase utama kontrol kongesti TCP klasik (Tahoe/Reno) adalah: **[Slow Start]** di man... | `tier-08::networking` |
| 11 | Foundational Definitions | Protokol transport modern berbasis UDP yang menyediakan enkripsi bawaan terintegrasi TL... | `tier-08::networking` |
| 12 | Foundational Definitions | Teorema CAP oleh Eric Brewer menyatakan bahwa sistem penyimpanan data terdistribusi han... | `tier-09::distributed` |
| 13 | Foundational Definitions | Teorema PACELC oleh Daniel Abadi memperluas teorema CAP: Jika terjadi Partisi (P), sist... | `tier-09::distributed` |
| 14 | Foundational Definitions | Tiga peran kemungkinan yang dapat diemban oleh sebuah simpul (node) dalam algoritma kon... | `tier-09::distributed` |
| 15 | Foundational Definitions | Invarian Pencocokan Log (Log Matching Invariant) pada Raft menjamin bahwa jika dua entr... | `tier-09::distributed` |
| 16 | Architecture Constants | Rentang waktu timeout pemilihan acak (Randomized Election Timeout) yang direkomendasika... | `tier-09::distributed` |
| 17 | Mathematical Identities | Mekanisme pelacakan kausalitas peristiwa parsial dalam sistem terdistribusi di mana set... | `tier-09::distributed` |
| 18 | Foundational Definitions | Algoritma partisi data terdistribusi yang memetakan node server dan key data ke dalam c... | `tier-09::distributed` |
| 19 | Foundational Definitions | Komponen in-memory pada storage engine Log-Structured Merge-Tree (LSM-Tree) yang menamp... | `tier-10::basis-data` |
| 20 | Foundational Definitions | File penyimpanan berbasis disk yang bersifat kekal (immutable) pada arsitektur LSM-Tree... | `tier-10::basis-data` |
| 21 | Foundational Definitions | Proses latar belakang pada LSM-Tree yang membaca beberapa file SSTable lama, membuang d... | `tier-10::basis-data` |
| 22 | Design Heuristics & Rules of Thumb | Perbandingan trade-off arsitektur penyimpanan: Pohon B-Tree mengorbankan performa penul... | `tier-10::basis-data` |
| 23 | Design Heuristics & Rules of Thumb | Prinsip desain sistem arsitektur jaringan yang menyatakan bahwa fungsi keandalan dan pe... | `tier-08::networking` |
| 24 | Assembly Opcodes & Byte Layouts | Instruksi vektor SIMD AVX2 x86 untuk mengeksekusi operasi perkalian dan penambahan floa... | `tier-08::dsp` |
| 25 | Foundational Definitions | Metode kontrol konkurensi basis data transaksional yang menyediakan setiap transaksi de... | `tier-10::basis-data` |

---

## Rincian Lengkap Kartu Spaced Repetition

### Kartu 01: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teorema Sampling Nyquist-Shannon menyatakan bahwa agar sinyal waktu-kontinu dengan frekuensi tertinggi f_{max} dapat direkonstruksi secara sempurna dari sampel diskritnya tanpa mengalami aliasing, frekuensi sampling f_s harus memenuhi syarat: {{c1::f_s \ge 2 f_{max}}} (di mana f_{Nyquist} = {{c2::2 f_{max}}}).

**Tampilan Jawaban Terbuka**:
> Teorema Sampling Nyquist-Shannon menyatakan bahwa agar sinyal waktu-kontinu dengan frekuensi tertinggi f_{max} dapat direkonstruksi secara sempurna dari sampel diskritnya tanpa mengalami aliasing, frekuensi sampling f_s harus memenuhi syarat: **[f_s \ge 2 f_{max]**} (di mana f_{Nyquist} = **[2 f_{max]**}).

**Penjelasan Ekstra & Konteks Teknis**:
> Jika frekuensi sampling di bawah batas ini, komponen frekuensi tinggi akan terlipat (aliased) ke dalam pita frekuensi rendah sebagai derau palsu.

**Tags**: `tier-08::dsp signals::nyquist-shannon foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 02: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Persamaan Transformasi Fourier Diskrit (Discrete Fourier Transform - DFT) untuk sinyal diskrit x[n] dengan panjang N sampel ke domain frekuensi X[k] dirumuskan sebagai: {{c1::X[k] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi}{N} k n}}}.

**Tampilan Jawaban Terbuka**:
> Persamaan Transformasi Fourier Diskrit (Discrete Fourier Transform - DFT) untuk sinyal diskrit x[n] dengan panjang N sampel ke domain frekuensi X[k] dirumuskan sebagai: **[X[k] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi}{N} k n]**}.

**Penjelasan Ekstra & Konteks Teknis**:
> Menghitung komponen spektral frekuensi diskrit. Komputasi langsung membutuhkan O(N^2) operasi aritmatika kompleks.

**Tags**: `tier-08::dsp signals::dft-formula mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 03: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Algoritma Fast Fourier Transform (FFT) Cooley-Tukey memangkas kompleksitas komputasi transformasi Fourier dari O(N^2) menjadi {{c1::O(N \log N)}} melalui teknik dekomposisi rekursif divide-and-conquer.

**Tampilan Jawaban Terbuka**:
> Algoritma Fast Fourier Transform (FFT) Cooley-Tukey memangkas kompleksitas komputasi transformasi Fourier dari O(N^2) menjadi **[O(N \log N)]** melalui teknik dekomposisi rekursif divide-and-conquer.

**Penjelasan Ekstra & Konteks Teknis**:
> Fondasi komputasi digital modern untuk pemrosesan radar, kompresi audio MP3/AAC, analisis citra medis, dan sintesis OFDM pada WiFi/5G.

**Tags**: `tier-08::dsp algorithms::fft mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 04: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Kapasitas kanal transmisi maksimum teoritis C dalam bit per detik pada kanal transmisi berpita frekuensi B yang mengalami derau Gaussian putih (AWGN) dirumuskan oleh Teorema Shannon-Hartley: {{c1::C = B \log_2 \left( 1 + \text{SNR} \right)}} (di mana SNR = {{c2::\frac{S}{N}}}).

**Tampilan Jawaban Terbuka**:
> Kapasitas kanal transmisi maksimum teoritis C dalam bit per detik pada kanal transmisi berpita frekuensi B yang mengalami derau Gaussian putih (AWGN) dirumuskan oleh Teorema Shannon-Hartley: **[C = B \log_2 \left( 1 + \text{SNR} \right)]** (di mana SNR = **[\frac{S}{N]**}).

**Penjelasan Ekstra & Konteks Teknis**:
> Menunjukkan bahwa kapasitas komunikasi data tidak hanya dibatasi oleh bandwidth frekuensi fisik (B), tetapi juga oleh rasio daya sinyal terhadap derau (SNR).

**Tags**: `tier-08::telekomunikasi information-theory::shannon mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 05: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran unit transmisi maksimum standar (Maximum Transmission Unit - MTU) pada jaringan Ethernet IEEE 802.3 adalah sebesar {{c1::1500 byte}}.

**Tampilan Jawaban Terbuka**:
> Ukuran unit transmisi maksimum standar (Maximum Transmission Unit - MTU) pada jaringan Ethernet IEEE 802.3 adalah sebesar **[1500 byte]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Jika paket IP berukuran lebih besar dari MTU hop berikutnya dan flag Don't Fragment (DF) aktif, router akan membuang paket dan mengirim pesan ICMP Fragmentation Needed.

**Tags**: `tier-08::networking protocols::ethernet-mtu architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 06: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Ukuran minimum header paket IPv4 standar tanpa opsi tambahan adalah {{c1::20 byte}}, dan ukuran minimum header segmen TCP standar tanpa opsi adalah {{c1::20 byte}}, menghasilkan overhead header transport gabungan minimum sebesar {{c2::40 byte}}.

**Tampilan Jawaban Terbuka**:
> Ukuran minimum header paket IPv4 standar tanpa opsi tambahan adalah **[20 byte]**, dan ukuran minimum header segmen TCP standar tanpa opsi adalah **[20 byte]**, menghasilkan overhead header transport gabungan minimum sebesar **[40 byte]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Sehingga Maximum Segment Size (MSS) efektif data TCP pada jaringan Ethernet MTU 1500 byte adalah: 1500 - 40 = 1460 byte.

**Tags**: `tier-08::networking protocols::headers architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 07: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Tiga langkah jabat tangan pembentukan koneksi TCP (Three-Way Handshake) secara berurutan adalah pertukaran paket: {{c1::SYN}} (klien menginisiasi sequence number x), {{c1::SYN-ACK}} (server mengakui x+1 dan mengirim sequence number y), dan {{c1::ACK}} (klien mengakui y+1).

**Tampilan Jawaban Terbuka**:
> Tiga langkah jabat tangan pembentukan koneksi TCP (Three-Way Handshake) secara berurutan adalah pertukaran paket: **[SYN]** (klien menginisiasi sequence number x), **[SYN-ACK]** (server mengakui x+1 dan mengirim sequence number y), dan **[ACK]** (klien mengakui y+1).

**Penjelasan Ekstra & Konteks Teknis**:
> Setelah pertukaran ini selesai, koneksi berada dalam status ESTABLISHED dan kedua belah pihak dapat mentransmisikan payload data.

**Tags**: `tier-08::networking protocols::tcp-handshake foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 08: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Status penutupan koneksi TCP di mana inisiator penutupan wajib menunggu selama durasi 2 * MSL (Maximum Segment Lifetime) sebelum membebaskan port socket disebut status {{c1::TIME_WAIT}}.

**Tampilan Jawaban Terbuka**:
> Status penutupan koneksi TCP di mana inisiator penutupan wajib menunggu selama durasi 2 * MSL (Maximum Segment Lifetime) sebelum membebaskan port socket disebut status **[TIME_WAIT]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Durasi TIME_WAIT (biasanya 60 detik) menjamin paket ACK penutupan terakhir sampai ke lawan bicara dan mencegah segmen data basi (delayed segments) mengkontaminasi koneksi baru.

**Tags**: `tier-08::networking protocols::time-wait architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 09: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Algoritma kontrol kongesti TCP CUBIC memodelkan pertumbuhan jendela kongesti (cwnd) sebagai fungsi pangkat tiga: {{c1::W_{cubic}(t) = C (t - K)^3 + W_{max}}}, di mana kurva berbentuk {{c2::konkaf mendekati W_{max} dan konveks setelah melampauinya}}.

**Tampilan Jawaban Terbuka**:
> Algoritma kontrol kongesti TCP CUBIC memodelkan pertumbuhan jendela kongesti (cwnd) sebagai fungsi pangkat tiga: **[W_{cubic}(t) = C (t - K)^3 + W_{max]**}, di mana kurva berbentuk **[konkaf mendekati W_{max} dan konveks setelah melampauinya]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Merupakan algoritma kongesti default di kernel Linux, dirancang khusus untuk stabilitas throughput tinggi pada jaringan Long-Fat Networks (bandwidth besar dengan RTT tinggi).

**Tags**: `tier-08::networking protocols::tcp-cubic mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 10: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Dua fase utama kontrol kongesti TCP klasik (Tahoe/Reno) adalah: {{c1::Slow Start}} di mana nilai cwnd berlipat ganda secara eksponensial setiap RTT (cwnd += MSS per ACK), dan {{c1::Congestion Avoidance}} di mana cwnd tumbuh secara linier (cwnd += MSS * (MSS/cwnd) per ACK).

**Tampilan Jawaban Terbuka**:
> Dua fase utama kontrol kongesti TCP klasik (Tahoe/Reno) adalah: **[Slow Start]** di mana nilai cwnd berlipat ganda secara eksponensial setiap RTT (cwnd += MSS per ACK), dan **[Congestion Avoidance]** di mana cwnd tumbuh secara linier (cwnd += MSS * (MSS/cwnd) per ACK).

**Penjelasan Ekstra & Konteks Teknis**:
> Titik transisi dari Slow Start ke Congestion Avoidance ditentukan oleh ambang batas slow start threshold (ssthresh).

**Tags**: `tier-08::networking protocols::slow-start foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 11: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Protokol transport modern berbasis UDP yang menyediakan enkripsi bawaan terintegrasi TLS 1.3, multiplexing multi-aliran tanpa Head-of-Line blocking, dan migrasi koneksi independen IP adalah {{c1::QUIC (fondasi protokol HTTP/3)}}.

**Tampilan Jawaban Terbuka**:
> Protokol transport modern berbasis UDP yang menyediakan enkripsi bawaan terintegrasi TLS 1.3, multiplexing multi-aliran tanpa Head-of-Line blocking, dan migrasi koneksi independen IP adalah **[QUIC (fondasi protokol HTTP/3)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> QUIC mendukung koneksi 0-RTT connection resumption, memangkas latensi pembukaan situs web berulang secara dramatis dibanding kombinasi TCP + TLS.

**Tags**: `tier-08::networking protocols::quic foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 12: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teorema CAP oleh Eric Brewer menyatakan bahwa sistem penyimpanan data terdistribusi hanya dapat menjamin maksimal dua dari tiga sifat secara bersamaan saat terjadi kegagalan jaringan: {{c1::Consistency (Konsistensi linier)}} , {{c1::Availability (Ketersediaan setiap request mendapat respon)}} , dan {{c1::Partition Tolerance (Toleransi partisi jaringan)}}.

**Tampilan Jawaban Terbuka**:
> Teorema CAP oleh Eric Brewer menyatakan bahwa sistem penyimpanan data terdistribusi hanya dapat menjamin maksimal dua dari tiga sifat secara bersamaan saat terjadi kegagalan jaringan: **[Consistency (Konsistensi linier)]** , **[Availability (Ketersediaan setiap request mendapat respon)]** , dan **[Partition Tolerance (Toleransi partisi jaringan)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Karena partisi fisik kabel jaringan terputus (P) tidak dapat dihindari di dunia nyata, arsitek sistem terdistribusi wajib memilih antara arsitektur CP atau AP.

**Tags**: `tier-09::distributed systems::cap-theorem foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 13: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Teorema PACELC oleh Daniel Abadi memperluas teorema CAP: Jika terjadi Partisi (P), sistem harus memilih antara {{c1::Availability (A)}} atau {{c1::Consistency (C)}}; Sedangkan dalam kondisi normal (Else - E), sistem harus memilih antara {{c1::Latency (L)}} atau {{c1::Consistency (C)}}.

**Tampilan Jawaban Terbuka**:
> Teorema PACELC oleh Daniel Abadi memperluas teorema CAP: Jika terjadi Partisi (P), sistem harus memilih antara **[Availability (A)]** atau **[Consistency (C)]**; Sedangkan dalam kondisi normal (Else - E), sistem harus memilih antara **[Latency (L)]** atau **[Consistency (C)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Contoh: MongoDB dan DynamoDB umumnya diklasifikasikan sebagai sistem PA/EL, sedangkan Dynamo (mode default) adalah PA/EC.

**Tags**: `tier-09::distributed systems::pacelc foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 14: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Tiga peran kemungkinan yang dapat diemban oleh sebuah simpul (node) dalam algoritma konsensus terdistribusi Raft adalah: {{c1::Leader}}, {{c1::Follower}}, dan {{c1::Candidate}}.

**Tampilan Jawaban Terbuka**:
> Tiga peran kemungkinan yang dapat diemban oleh sebuah simpul (node) dalam algoritma konsensus terdistribusi Raft adalah: **[Leader]**, **[Follower]**, dan **[Candidate]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dalam kondisi normal, terdapat tepat satu Leader yang melayani seluruh permintaan klien dan mereplikasi entri log ke seluruh node Follower.

**Tags**: `tier-09::distributed consensus::raft foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 15: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Invarian Pencocokan Log (Log Matching Invariant) pada Raft menjamin bahwa jika dua entri log pada server yang berbeda memiliki indeks dan term yang identik, maka: {{c1::keduanya menyimpan perintah mesin state yang sama persis}} dan {{c1::seluruh entri log pada indeks sebelumnya di kedua server dijamin identik}}.

**Tampilan Jawaban Terbuka**:
> Invarian Pencocokan Log (Log Matching Invariant) pada Raft menjamin bahwa jika dua entri log pada server yang berbeda memiliki indeks dan term yang identik, maka: **[keduanya menyimpan perintah mesin state yang sama persis]** dan **[seluruh entri log pada indeks sebelumnya di kedua server dijamin identik]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Invarian ini ditegakkan oleh konsistensi pengecekan pada RPC AppendEntries yang dikirimkan oleh Leader.

**Tags**: `tier-09::distributed consensus::raft-invariants foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 16: Architecture Constants

**Pertanyaan Cloze (Anki Text)**:
> Rentang waktu timeout pemilihan acak (Randomized Election Timeout) yang direkomendasikan pada algoritma Raft untuk mencegah fenomena split-vote berulang antar kandidat adalah berkisar antara {{c1::150 milidetik hingga 300 milidetik}}.

**Tampilan Jawaban Terbuka**:
> Rentang waktu timeout pemilihan acak (Randomized Election Timeout) yang direkomendasikan pada algoritma Raft untuk mencegah fenomena split-vote berulang antar kandidat adalah berkisar antara **[150 milidetik hingga 300 milidetik]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Pengacakan batas waktu timeout memastikan bahwa hampir selalu ada satu node yang timeout terlebih dahulu dan berhasil memenangkan mayoritas kuorum voting.

**Tags**: `tier-09::distributed consensus::raft-timeout architecture-constants`  
**Kategori**: `Architecture Constants`

---

### Kartu 17: Mathematical Identities

**Pertanyaan Cloze (Anki Text)**:
> Mekanisme pelacakan kausalitas peristiwa parsial dalam sistem terdistribusi di mana setiap simpul memelihara array counter logis berukuran N (jumlah proses) dinamakan {{c1::Vector Clocks (Jam Vektor)}}.

**Tampilan Jawaban Terbuka**:
> Mekanisme pelacakan kausalitas peristiwa parsial dalam sistem terdistribusi di mana setiap simpul memelihara array counter logis berukuran N (jumlah proses) dinamakan **[Vector Clocks (Jam Vektor)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Peristiwa A mendahului kausal peristiwa B (A -> B) jika dan hanya jika untuk setiap proses k, V(A)[k] <= V(B)[k], dan terdapat setidaknya satu elemen j di mana V(A)[j] < V(B)[j].

**Tags**: `tier-09::distributed causality::vector-clocks mathematical-identities`  
**Kategori**: `Mathematical Identities`

---

### Kartu 18: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Algoritma partisi data terdistribusi yang memetakan node server dan key data ke dalam cincin lingkaran hash [0 s/d 2^{128}-1] sehingga penambahan/pengurangan server hanya merelokasi fraksi K/N data disebut {{c1::Consistent Hashing}}.

**Tampilan Jawaban Terbuka**:
> Algoritma partisi data terdistribusi yang memetakan node server dan key data ke dalam cincin lingkaran hash [0 s/d 2^{128}-1] sehingga penambahan/pengurangan server hanya merelokasi fraksi K/N data disebut **[Consistent Hashing]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Penggunaan konsep Virtual Nodes (vnodes) menyeimbangkan distribusi beban data di seluruh server fisik dan mencegah munculnya hotspot partisi.

**Tags**: `tier-09::distributed hashing::consistent-hashing foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 19: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Komponen in-memory pada storage engine Log-Structured Merge-Tree (LSM-Tree) yang menampung operasi penulisan data terbaru dalam struktur data terurut (seperti SkipList atau Red-Black Tree) disebut {{c1::MemTable}}.

**Tampilan Jawaban Terbuka**:
> Komponen in-memory pada storage engine Log-Structured Merge-Tree (LSM-Tree) yang menampung operasi penulisan data terbaru dalam struktur data terurut (seperti SkipList atau Red-Black Tree) disebut **[MemTable]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Operasi penulisan ditulis terlebih dahulu ke Write-Ahead Log (WAL) di disk secara sekuensial sebelum dimasukkan ke MemTable untuk menjamin durabilitas ACID (Crash Recovery).

**Tags**: `tier-10::basis-data storage-engine::lsm-tree foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 20: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> File penyimpanan berbasis disk yang bersifat kekal (immutable) pada arsitektur LSM-Tree yang berisi entitas data key-value yang telah terurut secara leksikografis disebut {{c1::SSTable (Sorted String Table)}}.

**Tampilan Jawaban Terbuka**:
> File penyimpanan berbasis disk yang bersifat kekal (immutable) pada arsitektur LSM-Tree yang berisi entitas data key-value yang telah terurut secara leksikografis disebut **[SSTable (Sorted String Table)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> SSTable umumnya terdiri dari blok data terkompresi, blok indeks pencarian binary, dan filter probabilistik Bloom Filter.

**Tags**: `tier-10::basis-data storage-engine::sstable foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 21: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Proses latar belakang pada LSM-Tree yang membaca beberapa file SSTable lama, membuang data duplikat/tombstone yang telah dihapus, menggabungkan data secara terurut, dan menuliskan SSTable baru ke level berikutnya dinamakan proses {{c1::Compaction}}.

**Tampilan Jawaban Terbuka**:
> Proses latar belakang pada LSM-Tree yang membaca beberapa file SSTable lama, membuang data duplikat/tombstone yang telah dihapus, menggabungkan data secara terurut, dan menuliskan SSTable baru ke level berikutnya dinamakan proses **[Compaction]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Dua strategi utama pemadatan adalah Size-Tiered Compaction Strategy (STCS - optimal untuk beban write) dan Leveled Compaction Strategy (LCS - optimal untuk latensi read).

**Tags**: `tier-10::basis-data storage-engine::compaction foundational-definitions`  
**Kategori**: `Foundational Definitions`

---

### Kartu 22: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Perbandingan trade-off arsitektur penyimpanan: Pohon B-Tree mengorbankan performa penulisan untuk mencapai {{c1::amplifikasi penulisan (Write Amplification) tinggi akibat random writes}} demi keunggulan {{c2::latensi pembacaan titik tunggal (point reads) yang rendah}}, sedangkan LSM-Tree mengoptimalkan penulisan sekuensial cepat dengan konsekuensi {{c2::amplifikasi pembacaan (Read Amplification) lebih tinggi}}.

**Tampilan Jawaban Terbuka**:
> Perbandingan trade-off arsitektur penyimpanan: Pohon B-Tree mengorbankan performa penulisan untuk mencapai **[amplifikasi penulisan (Write Amplification) tinggi akibat random writes]** demi keunggulan **[latensi pembacaan titik tunggal (point reads) yang rendah]**, sedangkan LSM-Tree mengoptimalkan penulisan sekuensial cepat dengan konsekuensi **[amplifikasi pembacaan (Read Amplification) lebih tinggi]**.

**Penjelasan Ekstra & Konteks Teknis**:
> B-Tree adalah standar pada RDBMS transaksional (PostgreSQL/MySQL InnoDB), sedangkan LSM-Tree mendominasi storage engine modern (RocksDB, Cassandra, TiKV).

**Tags**: `tier-10::basis-data storage::btree-vs-lsm design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 23: Design Heuristics & Rules of Thumb

**Pertanyaan Cloze (Anki Text)**:
> Prinsip desain sistem arsitektur jaringan yang menyatakan bahwa fungsi keandalan dan pengecekan integritas harus ditempatkan pada titik akhir aplikasi (end-to-end), bukan di dalam infrastruktur komunikasi perantara adalah {{c1::End-to-End Principle (Saltzer, Reed, Clark)}}.

**Tampilan Jawaban Terbuka**:
> Prinsip desain sistem arsitektur jaringan yang menyatakan bahwa fungsi keandalan dan pengecekan integritas harus ditempatkan pada titik akhir aplikasi (end-to-end), bukan di dalam infrastruktur komunikasi perantara adalah **[End-to-End Principle (Saltzer, Reed, Clark)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Menjelaskan mengapa keandalan TCP dan enkripsi TLS ditempatkan pada host ujung, bukan pada router perantara IP.

**Tags**: `tier-08::networking architecture::end-to-end design-heuristics`  
**Kategori**: `Design Heuristics & Rules of Thumb`

---

### Kartu 24: Assembly Opcodes & Byte Layouts

**Pertanyaan Cloze (Anki Text)**:
> Instruksi vektor SIMD AVX2 x86 untuk mengeksekusi operasi perkalian dan penambahan float32 berpresisi tinggi dalam satu langkah pipa hardware tanpa pembulatan perantara adalah {{c1::vfmadd231ps (Fused Multiply-Accumulate)}}.

**Tampilan Jawaban Terbuka**:
> Instruksi vektor SIMD AVX2 x86 untuk mengeksekusi operasi perkalian dan penambahan float32 berpresisi tinggi dalam satu langkah pipa hardware tanpa pembulatan perantara adalah **[vfmadd231ps (Fused Multiply-Accumulate)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Mengeksekusi operasi `d = (a * b) + c` pada 8 angka float32 secara serentak dalam register 256-bit YMM dalam hitungan ~4 siklus clock.

**Tags**: `tier-08::dsp x86::simd-avx2 assembly-opcodes`  
**Kategori**: `Assembly Opcodes & Byte Layouts`

---

### Kartu 25: Foundational Definitions

**Pertanyaan Cloze (Anki Text)**:
> Metode kontrol konkurensi basis data transaksional yang menyediakan setiap transaksi dengan snapshot konsisten basis data pada saat transaksi dimulai tanpa mengunci pembacaan data dinamakan {{c1::MVCC (Multi-Version Concurrency Control)}}.

**Tampilan Jawaban Terbuka**:
> Metode kontrol konkurensi basis data transaksional yang menyediakan setiap transaksi dengan snapshot konsisten basis data pada saat transaksi dimulai tanpa mengunci pembacaan data dinamakan **[MVCC (Multi-Version Concurrency Control)]**.

**Penjelasan Ekstra & Konteks Teknis**:
> Diimplementasikan dengan menyimpan versi record tuple menggunakan penanda waktu xmin (ID transaksi pembuat) dan xmax (ID transaksi penghapus) seperti pada PostgreSQL.

**Tags**: `tier-10::basis-data concurrency::mvcc foundational-definitions`  
**Kategori**: `Foundational Definitions`

---
