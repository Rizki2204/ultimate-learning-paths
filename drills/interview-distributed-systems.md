# Simulasi Wawancara Teknis L6 Staff: Arsitektur Sistem Terdistribusi & Komputasi Awan (Cloud Architect)

**Berkas**: `interview-distributed-systems.md`  
**Target Peran**: Staff / Principal Distributed Systems & Cloud Architect (L6 / E6 / IC6)  
**Trek Terkait**: [`track-distributed-systems-cloud-architect.md`](../tracks/track-distributed-systems-cloud-architect.md)  
**Tingkat Kurikulum**: [Tingkat 9: Rekayasa Software & Cloud SRE](../curriculum/09-software-engineering-cloud-sre/README.md) & [Tingkat 10: Basis Data Enterprise](../curriculum/10-basis-data-enterprise/README.md)  
**Deck Flashcards Terkait**: [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md)

---

## 1. Profil Evaluasi Kandidat Staff L6 (Competency Rubric)

Peran Staff Distributed Systems & Cloud Architect (L6) bertanggung jawab atas keandalan, elastisitas, dan konsistensi data dari platform hyperscale yang melayani puluhan juta permintaan per detik melintasi pusat data global. Wawancara ini menguji penguasaan teori konsensus, pemodelan kausalitas terdistribusi, mitigasi kegagalan partisi jaringan (*network partition / split-brain*), dan perancangan arsitektur basis data terdistribusi multi-wilayah.

### Dimensi Penilaian Utama:
1. **Teori Konsensus & Replikasi Data**: Penguasaan mendalam atas protokol Raft, Paxos, Multi-Raft, rekonfigurasi keanggotaan klaster (*Joint Consensus*), dan *Paxos Leases*.
2. **Kausalitas Waktu & Linearizability**: Perbandingan Google TrueTime API (GPS + Atomic Clocks) vs Hybrid Logical Clocks (HLC) dan Vector Clocks dalam menegakkan isolasi transaksi *Strict Serializable*.
3. **Ketahanan Arsitektur Terhadap Kegagalan (Resilience & Chaos)**: Desain pencegahan Split-Brain, Fencing Tokens, penanganan latensi ekor terdistribusi (*Tail Latency Hedged Requests*), dan partisi multi-region.
4. **Penyimpanan Terdistribusi Skala Global**: Partisi shard dinamis, replikasi kuorum, dan mitigasi *Compaction Debt* pada sistem berbasis LSM-Tree (seperti TiKV atau CockroachDB).

---

## 2. Bagian 1: Skenario Arsitektur & Interogasi Sokratik (4 Soal L6)

### Skenario 1.1: Rekonfigurasi Keanggotaan Klaster Dinamis: Joint Consensus pada Multi-Raft
**Masalah Kasus Nyata**:  
Sebuah klaster database terdistribusi Multi-Raft (seperti TiKV atau CockroachDB) menjalankan 3 node replika di Wilayah US-East. Tim arsitektur ingin menambahkan 2 node baru di Wilayah US-West secara live di produksi tanpa menghentikan kueri transaksi tulis (*zero-downtime membership change* dari 3 node ke 5 node).

Sebagai Staff Distributed Systems Architect, jelaskan:
1. Mengapa beralih langsung secara naif dari konfigurasi lama $C_{\text{old}} = \{1, 2, 3\}$ ke konfigurasi baru $C_{\text{new}} = \{1, 2, 3, 4, 5\}$ dalam satu langkah pembaruan dapat memicu terbentuknya **dua kuorum mayoritas yang saling terisolasi (Split-Brain)**?
2. Bagaimana mekanisme **Joint Consensus** karya Diego Ongaro memecahkan masalah ini dengan menegakkan fase transisi konfigurasi gabungan $C_{\text{old,new}}$ di mana persetujuan kuorum wajib diraih dari KEDUA kubu secara simultan?
3. Apa perbedaan pendekatan Joint Consensus dua fase terhadap pendekatan penambahan simpul satu-per-satu (*single-server membership change*)?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Bahaya Transisi Konfigurasi Langsung Satu Langkah**:
   - Dalam sistem terdistribusi asinkron, pesan log replikasi tidak tiba di seluruh simpul pada saat yang bersamaan.
   - Misalkan Pemimpin mengirimkan pesan perubahan konfigurasi dari $C_{\text{old}} = \{1, 2, 3\}$ ke $C_{\text{new}} = \{1, 2, 3, 4, 5\}$.
   - Node 1 dan 2 menerima pesan dan beralih ke $C_{\text{new}}$ (di mana kuorum mayoritas adalah 3 dari 5 node).
   - Node 3 belum menerima pesan akibat penundaan jaringan dan tetap menganggap konfigurasi adalah $C_{\text{old}}$ (di mana kuorum mayoritas adalah 2 dari 3 node).
   - **Bencana Split-Brain**:
     - Node 1, 4, dan 5 dapat memilih pemimpin baru di bawah aturan $C_{\text{new}}$ (3 dari 5 node).
     - Secara simultan, Node 2 dan 3 dapat memilih pemimpin lain di bawah aturan $C_{\text{old}}$ (2 dari 3 node).
     - Dua pemimpin sah terpilih secara bersamaan, memicu percabangan log data yang korup dan tidak dapat direkonsiliasi.
2. **Protokol Transisi Dua Fase Joint Consensus**:
   - **Fase 1 (Konfigurasi Gabungan $C_{\text{old,new}}$)**:
     - Pemimpin menulis entri log konfigurasi transisi $C_{\text{old,new}}$ dan mereplikasikannya ke seluruh node.
     - Di bawah $C_{\text{old,new}}$, keputusan komit dan pemilihan pemimpin **wajib mendapatkan persetujuan mayoritas dari $C_{\text{old}}$ DAN mayoritas dari $C_{\text{new}}$ secara terpisah**:
       $$\text{Kuorum} = \text{Mayoritas}(C_{\text{old}}) \land \text{Mayoritas}(C_{\text{new}})$$
     - Karena kuorum $C_{\text{old}}$ selalu beririsan dengan kuorum $C_{\text{old}}$ lainnya, mustahil terbentuk dua pemimpin terpisah selama fase ini.
   - **Fase 2 (Konfigurasi Akhir $C_{\text{new}}$)**:
     - Begitu entri $C_{\text{old,new}}$ berhasil di-commit (telah direplikasi ke mayoritas kedua kubu), pemimpin menulis entri konfigurasi final $C_{\text{new}}$.
     - Setelah $C_{\text{new}}$ di-commit, node lama yang tidak terpakai dipensiunkan secara aman.
3. **Joint Consensus vs Single-Server Changes**:
   - *Single-Server Changes* (Raft Bagian 4.3) hanya mengizinkan penambahan atau pengurangan tepat 1 node per langkah ($N \to N+1$). Secara matematis, dua kuorum mayoritas dari konfigurasi $N$ dan $N+1$ dijamin selalu memiliki irisan minimal 1 node.
   - Namun, penambahan 2 node baru lintas region harus dilakukan dalam 2 langkah serial terpisah yang memakan waktu lama. Joint Consensus lebih fleksibel karena mampu mengeksekusi migrasi konfigurasi sembarang (misal memindahkan seluruh klaster dari Region A ke Region B) dalam satu prosedur transaksi yang aman.
</details>

---

### Skenario 1.2: Sinkronisasi Waktu Global: Google TrueTime vs Hybrid Logical Clocks (HLC)
**Masalah Kasus Nyata**:  
Sebuah institusi perbankan global menuntut basis data transaksi finansial terdistribusi multi-wilayah yang menjamin konsistensi **Strict Serializability / Linearizability**: jika transaksi $T_2$ dimulai setelah transaksi $T_1$ selesai di-commit di belahan dunia lain, timestamp commit transaksi $T_2$ wajib lebih besar dari $T_1$ ($t_{c2} > t_{c1}$).

Jelaskan:
1. Mengapa sinkronisasi jam dinding fisik via protokol NTP standar (dengan jitter deviasi $\pm 50\text{ ms}$) tidak mampu menegakkan urutan transaksi linearizable tanpa penguncian global yang lambat?
2. Bagaimana arsitektur **Google TrueTime API** pada Google Spanner merepresentasikan waktu sebagai interval ketidakpastian $[t_{\text{earliest}}, t_{\text{latest}}]$ dengan batas kesalahan terikat $\epsilon \approx 1-7\text{ ms}$, dan bagaimana aturan **Commit Wait** menjamin keterurutan linearitas mutlak?
3. Bagaimana database terdistribusi komersial open-source (seperti CockroachDB atau YugabyteDB) mengimplementasikan **Hybrid Logical Clocks (HLC)** untuk mencapai isolasi serializable di atas infrastruktur komputasi awan komersial standar tanpa perangkat keras GPS dan jam atomik fisik?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Kerapuhan NTP untuk Linearizability**:
   - Jam dinding kuarsa fisik di server mengalami pergeseran (*drift*). NTP menyinkronkan jam melalui jaringan dengan ketidakpastian hingga puluhan milidetik.
   - Jika Transaksi $T_1$ di-commit di Server Tokyo pada jam lokal $12:00:00.040$, lalu memberi sinyal ke pengguna, dan pengguna tersebut memicu Transaksi $T_2$ di Server New York:
   - Jika jam New York tertinggal 50 ms, New York dapat memberikan timestamp commit $12:00:00.010$ untuk $T_2$.
   - Di mata sistem, $T_2$ tampak terjadi SEBELUM $T_1$, melanggar kausalitas dan integritas saldo rekening perbankan.
2. **Arsitektur Google TrueTime & Commit Wait**:
   - Google melengkapi setiap data center dengan penerima GPS fisik dan jam atomik Rubidium independen.
   - TrueTime API tidak mengembalikan angka skalar tunggal, melainkan interval waktu:
     $$\text{TT.now}() = [t_{\text{earliest}}, t_{\text{latest}}], \quad \text{di mana } t_{\text{latest}} - t_{\text{earliest}} = 2\epsilon \quad (\epsilon \le 7\text{ ms})$$
   - Waktu absolut riil dijamin berada di dalam interval tersebut.
   - **Aturan Commit Wait Spanner**:
     Ketika sebuah transaksi meminta commit, koordinator memilih timestamp commit $s = t_{\text{latest}}$.
     Koordinator menahan respons ke klien dan sengaja tidur (*sleep/commit wait*) sampai:
     $$\text{TT.now}().\text{earliest} > s$$
     Durasi tidur adalah sebesar $2\epsilon$ (sekitar 7-14 ms).
     Ketika respons akhirnya diserahkan ke pengguna, waktu riil di seluruh alam semesta **dijamin secara fisik telah melampaui timestamp $s$**. Transaksi berikutnya di manapun di muka bumi pasti mendapatkan timestamp $> s$, menegakkan linearizability mutlak tanpa perlu koordinasi lintas benua.
3. **Hybrid Logical Clocks (HLC)**:
   - Klaster cloud publik AWS/GCP tidak menyediakan hardware jam atomik TrueTime untuk VM pengguna.
   - HLC memadukan pembacaan jam fisik lokal ($pt$) dan pencacah logis Lamport ($l, c$):
     $$\text{HLC} = (l, c) \quad \text{di mana } l \approx pt \text{ dan } c \text{ adalah counter kejadian kausal}$$
   - Ketika simpul menerima pesan dari simpul lain dengan timestamp HLC lebih tinggi, simpul memajukan nilai $l$-nya: $l_{\text{new}} = \max(l_{\text{local}}, pt_{\text{local}}, l_{\text{msg}})$.
   - HLC menjamin kausalitas: jika $e_1 \to e_2$, maka $\text{HLC}(e_1) < \text{HLC}(e_2)$, sekaligus menjaga nilai fisik $l$ tetap berada dalam batas toleransi offset jam NTP maksimal (misal $\Delta_{\max} = 500\text{ ms}$). Jika penyimpangan jam melebihi batas toleransi, node mematikan dirinya sendiri (*crash node*) untuk melindungi integritas transaksi.
</details>

---

### Skenario 1.3: Mitigasi Split-Brain Jaringan: Fencing Tokens & Leaseholder Architecture
**Masalah Kasus Nyata**:  
Sebuah layanan penyimpanan penyimpanan terdistribusi menggunakan mekanisme *Master-Worker* dengan Apache ZooKeeper untuk memilih satu simpul Master aktif. Master 1 mengalami *Garbage Collection (GC) Pause* durasi panjang selama 45 detik. ZooKeeper menganggap Master 1 telah mati karena heartbeat timeout, lalu memilih Master 2 sebagai Master baru. Tepat setelah Master 2 mengambil alih, GC Pause pada Master 1 berakhir dan Master 1 terbangun, meyakini dirinya masih merupakan Master yang sah (*Zombie Master*). KEDUA master serentak mengirimkan instruksi penulisan ke sistem penyimpanan disk bersama (*Shared Storage*).

Jelaskan:
1. Mengapa penguncian terdistribusi standar (*distributed locks*) tanpa token pelindung tidak mampu mencegah kerusakan data pada skenario ini?
2. Bagaimana mekanisme **Fencing Tokens** (nomor generasi monoton bertambah) membatalkan instruksi dari Master Zombie secara otomatis di tingkat subsistem penyimpanan?
3. Bagaimana arsitektur modern berbasis **Paxos Leases** memastikan bahwa sebuah simpul tidak akan pernah mengeksekusi operasi master jika batas sewa waktu fisiknya telah kadaluwarsa?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Kegagalan Kunci Terdistribusi Sederhana**:
   - Kunci terdistribusi yang diperoleh dari ZooKeeper atau Redis/Redlock hanya melindungi status kepemilikan di sisi koordinator.
   - Master 1 memperoleh lock. Master 1 membaca status, lalu terjebak dalam GC pause panjang.
   - Lock kadaluwarsa. Master 2 memperoleh lock baru dan menulis data ke storage.
   - Master 1 terbangun dari GC pause. Master 1 melanjutkan instruksi penulisan yang tertunda dan mengirimkannya ke storage.
   - Paket dari Master 1 tiba di storage setelah Master 2 menulis, menimpa dan mengorup data baru tanpa ada mekanisme penguncian yang mampu mendeteksinya.
2. **Mekanisme Fencing Tokens**:
   - Setiap kali sebuah lock atau kepemimpinan master diberikan oleh server konsensus, server menyertakan **Fencing Token**: bilangan bulat yang dijamin meningkat secara monoton ($1, 2, 3, \dots$).
   - Master 1 menerima Token $= 33$.
   - Saat Master 1 mengalami jeda GC, lock lepas. Master 2 terpilih dan menerima Token $= 34$.
   - Master 2 menulis ke storage dengan menyertakan tokennya: `write(data, token=34)`.
   - Subsistem penyimpanan merekam token tertinggi yang pernah dilihatnya: $\text{highest\_seen\_token} = 34$.
   - Ketika Master 1 terbangun dan mengirimkan instruksi lamanya: `write(data, token=33)`.
   - Storage memeriksa kondisi pagar (*fencing check*): karena $33 < 34$, storage **langsung menolak instruksi Master 1 dengan pesan error `STALE_FENCING_TOKEN`**.
   - Integritas data terlindungi secara mutlak tanpa bergantung pada ketepatan waktu prosesor.
3. **Paxos Leases**:
   - Dalam sistem Multi-Raft modern, hak melayani kueri baca lokal tanpa putaran konsensus (*LeaseRead*) diikat oleh kontrak sewa waktu (*lease*).
   - Pemimpin kuorum memegang sewa dari pengikutnya untuk durasi tertentu (misal 5 detik).
   - Pengikut berjanji tidak akan memilih pemimpin baru selama periode sewa tersebut masih berlaku.
   - Pemimpin secara terus menerus memperbarui sewanya. Jika terjadi partisi jaringan atau GC pause dan pemimpin tidak dapat memperbarui sewa, pemimpin secara otomatis **melepas hak kepemimpinannya sendiri secara sukarela sebelum simpul lain diizinkan memilih pemimpin baru**, mengeliminasi peluang master zombie secara proaktif.
</details>

---

### Skenario 1.4: Mitigasi Latensi Ekor Terdistribusi: Hedged Requests & Tail Tolerance
**Masalah Kasus Nyata**:  
Sebuah mesin pencari web modern mengeksekusi satu kueri pengguna dengan menyebarkannya (*fan-out*) ke 100 node shard indeks secara paralel, lalu menggabungkan hasilnya (*scatter-gather*). Meskipun setiap node shard memiliki latensi rata-rata $10\text{ ms}$ dengan latensi persentil $p99 = 1000\text{ ms}$ ($1\text{ detik}$), latensi kueri yang dialami pengguna akhir hampir selalu di atas $1\text{ detik}$ pada lebih dari $63\%$ kueri!

Jelaskan:
1. Turunkan secara matematis bagaimana probabilitas latensi ekor terdistribusi meledak seiring dengan bertambahnya faktor fan-out sub-layanan ($P_{\text{tail}} = 1 - (1 - p)^M$).
2. Bagaimana teknik **Hedged Requests** karya Jeffrey Dean (Google) memotong latensi ekor $p99$ hingga $80\%$ dengan hanya menambah overhead beban jaringan sebesar $2-5\%$?
3. Mengapa penambahan batas timeout agresif (*aggressive timeout & immediate retry*) justru dapat meruntuhkan seluruh sistem melalui badai beban berantai (*cascading failure*), dan bagaimana *Cross-Request Cancellation* memitigasi hal ini?

<details>
<summary><b>🔍 Buka Solusi Sokratik & Analisis Arsitektural Staff L6</b></summary>

**Analisis Tingkat Staf**:
1. **Ledakan Latensi Ekor Scatter-Gather**:
   - Jika sebuah permintaan pengguna bergantung pada $M = 100$ shard paralel, permintaan pengguna hanya selesai jika **SELURUH 100 shard** telah mengembalikan respons:
     $$T_{\text{user}} = \max(T_1, T_2, \dots, T_{100})$$
   - Misalkan probabilitas sebuah shard mengalami degradasi latensi p99 adalah $p = 0{,}01$ (1%).
   - Probabilitas bahwa seluruh 100 shard berhasil merespons dengan cepat tanpa ada satupun yang lambat adalah:
     $$P(\text{semua cepat}) = (1 - p)^M = (1 - 0{,}01)^{100} = (0{,}99)^{100} \approx 0{,}366 \ (36{,}6\%)$$
   - Probabilitas kueri pengguna mengalami keterlambatan latensi ekor $p99$:
     $$P_{\text{tail}} = 1 - (1 - p)^M = 1 - 0{,}366 = \mathbf{0{,}634 \ (63{,}4\%)}!$$
   - Meskipun hanya 1% permintaan individu yang lambat, **63,4% pengguna akhir menderita kelambatan 1 detik** murni akibat efek multiplikasi fan-out paralel!
2. **Teknik Hedged Requests (Google Tail-Tolerance)**:
   - Kirim permintaan awal ke replika primer shard.
   - Pantau latensi: jika replika primer tidak mengembalikan respons dalam persentil ke-95 waktu normal (misal setelah $15\text{ ms}$):
   - Kirim permintaan duplikat kedua (*hedged request*) ke replika cadangan di node yang berbeda.
   - Gunakan respons dari replika mana pun yang tiba lebih dulu.
   - Karena kemungkinan kedua replika independen mengalami outlier latensi p99 secara serentak sangat kecil ($p^2 = 0{,}01 \times 0{,}01 = 0{,}0001 = 0{,}01\%$), latensi ekor p99 seketika terpangkas dari $1000\text{ ms}$ menjadi sekitar $25\text{ ms}$.
   - Beban tambahan pada klaster hanya sebesar $5\%$ (karena hedged request hanya dikirimkan pada 5% kueri yang lambat).
3. **Cross-Request Cancellation**:
   - Melakukan retry membabi-buta tanpa pembatalan akan melipatgandakan beban server yang sedang tercekik.
   - Begitu respons pertama tiba dari salah satu replika, klien wajib mengirimkan pesan pembatalan (*cancellation token*) ke replika lainnya untuk menghentikan pemrosesan kueri di memori/disk worker tersebut, membebaskan thread worker dari pemborosan siklus komputasi.
</details>

---

## 3. Bagian 2: Penurunan Matematis & Analisis Kuantitatif Sistem Terdistribusi (2 Soal)

### Soal 2.1: Bukti Batas Toleransi Kesalahan Byzantine (BFT) $N \ge 3f + 1$ vs Crash Fault Tolerance (CFT) $N \ge 2f + 1$
Dalam sistem terdistribusi berisi $N$ node di mana maksimal $f$ node dapat mengalami kegagalan:
1. Buktikan secara matematis mengapa untuk sistem dengan model kegagalan henti (*Crash-Fault-Tolerant - CFT*, seperti Paxos dan Raft), jumlah simpul minimum yang dibutuhkan adalah:
   $$N_{\text{CFT}} = 2f + 1$$
2. Dalam model kegagalan acak/jahat (*Byzantine Fault Tolerance - BFT*, seperti PBFT), buktikan bahwa sistem membutuhkan minimal:
   $$N_{\text{BFT}} = 3f + 1$$
   simpul untuk mencapai konsensus. Tunjukkan argumen matematis Lamport, Shostak, dan Pease (1982) di mana jika $N = 3$ dan $f = 1$, komandan atau letnan pengkhianat dapat memecah belah keputusan klaster secara tak terelakkan.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Kasus Crash Fault Tolerance (CFT)**:
- Dalam model CFT, node yang gagal hanya berhenti merespons (*fail-stop*), tidak pernah mengirimkan pesan palsu atau berbohong.
- Jika terdapat $f$ node yang mati, tersisa $N - f$ node yang masih aktif merespons.
- Agar sistem dapat terus membuat kemajuan (*liveness*), kuorum harus dapat dibentuk dari node yang masih hidup:
  $$\text{Ukuran Kuorum } Q \le N - f$$
- Agar dua kuorum yang berbeda dijamin selalu memiliki irisan minimal satu node yang jujur (*safety / quorum intersection property*):
  $$Q_1 \cap Q_2 \ne \emptyset \implies 2Q - N \ge 1 \implies 2Q \ge N + 1 \implies Q \ge \frac{N + 1}{2}$$
- Gabungkan kedua batasan:
  $$\frac{N + 1}{2} \le Q \le N - f \implies \frac{N + 1}{2} \le N - f$$
  $$N + 1 \le 2N - 2f \implies N \ge 2f + 1$$
Terbukti bahwa untuk menoleransi $f$ crash node, sistem CFT membutuhkan minimal $2f + 1$ node (misal untuk menoleransi 1 crash node dibutuhkan $2(1) + 1 = 3$ node).

**Langkah 2: Kasus Byzantine Fault Tolerance (BFT)**:
Dalam model BFT, $f$ node yang korup/jahat dapat berbohong secara aktif, memancarkan pesan yang saling bertentangan ke node berbeda, atau berkolusi.
- Dari total $N$ node, terdapat $f$ node pengkhianat (*byzantine nodes*).
- Node jujur yang aktif merespons bisa saja terlambat akibat penundaan jaringan asinkron, sehingga sistem tidak dapat membedakan antara node yang mati dan node yang lambat.
- Sistem harus mampu mengambil keputusan hanya berdasarkan $N - f$ respons pertama yang tiba:
  $$\text{Ukuran Kuorum Respons } Q = N - f$$
- Di dalam $N - f$ respons yang diterima tersebut, kemungkinan terburuknya adalah seluruh $f$ node jahat telah membalas secara licik, sehingga jumlah respons dari node jujur murni hanya sebanyak:
  $$N_{\text{jujur}} = (N - f) - f = N - 2f$$
- Agar node jujur dapat membentuk konsensus mayoritas yang tidak dapat digoyahkan oleh kebohongan $f$ node jahat:
  Jumlah respons jujur ($N - 2f$) harus **lebih banyak** daripada jumlah node jahat ($f$):
  $$N - 2f > f \implies N > 3f \implies N \ge 3f + 1$$

**Langkah 3: Pembuktian Ketidakmungkinan untuk $N = 3$ dan $f = 1$**:
Misalkan terdapat 3 simpul: Komandan $C$, Letnan $L_1$, dan Letnan $L_2$. Satu simpul adalah pengkhianat ($f = 1$).
- **Skenario A (Letnan $L_2$ adalah Pengkhianat)**:
  - Komandan $C$ (jujur) mengirimkan perintah "SERANG" ke $L_1$ dan $L_2$.
  - Letnan $L_2$ (pengkhianat) berbohong dan melapor ke $L_1$: *"Komandan memerintahkan saya untuk MUNDUR"*.
  - Di mata $L_1$, ia menerima 1 suara SERANG (dari $C$) dan 1 suara MUNDUR (dari $L_2$).
- **Skenario B (Komandan $C$ adalah Pengkhianat)**:
  - Komandan $C$ (pengkhianat) mengirimkan perintah "SERANG" ke $L_1$, tetapi mengirimkan perintah "MUNDUR" ke $L_2$.
  - Letnan $L_2$ (jujur) melapor ke $L_1$: *"Komandan memerintahkan saya untuk MUNDUR"*.
  - Di mata $L_1$, ia menerima 1 suara SERANG (dari $C$) dan 1 suara MUNDUR (dari $L_2$).
- **Kesimpulan Kontradiksi**:
  Pandangan $L_1$ pada Skenario A dan Skenario B **identik secara simetris**. $L_1$ tidak memiliki cara matematis untuk membedakan apakah Komandan yang berbohong atau Letnan $L_2$ yang berbohong.
  Konsensus mustahil tercapai jika $N \le 3f$. Sistem BFT menuntut minimal $N = 3(1) + 1 = \mathbf{4\text{ node}}$ untuk menoleransi 1 node pengkhianat.
</details>

---

### Soal 2.2: Bukti Matematis Ketiadaan Pembacaan Hantu pada Algoritma Read-Index Raft
Dalam protokol konsensus Raft klasik, melayani kueri baca (*Read Request*) dengan menuliskan entri log baru ke disk memakan biaya penulisan disk dan putaran konsensus penyiaran penuh.
Algoritma optimasi **Read-Index** mengizinkan pemimpin melayani pembacaan langsung dari memori tanpa menulis log baru:
1. Pemimpin mencatat indeks komit saat ini: $\text{read\_index} = \text{commit\_index}$.
2. Pemimpin mengirimkan pesan detak jantung kosong (*heartbeat*) ke seluruh pengikut untuk mengonfirmasi bahwa dirinya masih merupakan pemimpin sah yang memegang kuorum mayoritas.
3. Pemimpin menunggu hingga mesin status lokalnya (*State Machine*) telah menerapkan seluruh entri hingga $\text{last\_applied} \ge \text{read\_index}$.
4. Pemimpin membaca data dari state machine dan mengembalikan respons ke klien.
Buktikan secara formal bahwa algoritma Read-Index menjamin **Linearizable Reads** dan mencegah pembacaan data basi (*stale reads*) bahkan jika telah terjadi partisi jaringan yang memilih pemimpin baru di kubu lain.

<details>
<summary><b>📐 Buka Penurunan Matematis Lengkap & Pembuktian</b></summary>

**Langkah 1: Definisi Formal Konsistensi Linearizable**:
Sebuah operasi baca $R$ bersifat linearizable jika ia mengembalikan nilai dari operasi tulis terakhir $W$ yang mendahuluinya dalam tatanan waktu global riil (*real-time precedence order*), dan tidak ada pembacaan berikutnya yang mengembalikan nilai yang lebih tua.

**Langkah 2: Verifikasi Kepemimpinan Aktif pada Waktu Baca**:
- Masalah utama pembacaan lokal pada pemimpin adalah keberadaan **Stale Leader**: pemimpin yang terisolasi oleh partisi jaringan dan telah digantikan oleh pemimpin baru di partisi mayoritas, namun belum menyadarinya.
- Pada Langkah 2, pemimpin mengirimkan paket heartbeat ke seluruh klaster dan menuntut konfirmasi acknowledgment dari **Kuorum Mayoritas** node ($Q \ge \lfloor N/2 \rfloor + 1$).
- Jika sebuah pemimpin baru telah terpilih di partisi lain, pemimpin baru tersebut pasti terpilih pada Term yang lebih tinggi ($\text{term}_{\text{new}} > \text{term}_{\text{old}}$) melalui dukungan kuorum mayoritas node.
- Berdasarkan Teorema Irisan Kuorum, kuorum heartbeat dari pemimpin lama dan kuorum pemilihan dari pemimpin baru **pasti memiliki irisan minimal satu node**:
  $$Q_{\text{heartbeat}} \cap Q_{\text{election}} \ne \emptyset$$
- Node pada irisan tersebut akan menolak heartbeat dari pemimpin lama karena term-nya telah kadaluwarsa, atau membalas dengan term baru yang memaksa pemimpin lama seketika turun takhta menjadi pengikut (*step down*).
- Oleh karena itu, keberhasilan pengumpulan kuorum heartbeat pada saat $t_{\text{read}}$ membuktikan secara matematis bahwa **TIDAK ADA pemimpin lain yang sah di seluruh sistem pada saat tersebut**.

**Langkah 3: Jaminan Monotonik Status Mesin (Step 3)**:
- Nilai $\text{read\_index}$ merepresentasikan batas komit yang telah disepakati oleh kuorum pada saat kueri baca diterima.
- Dengan menunggu kondisi $\text{last\_applied} \ge \text{read\_index}$:
  Pemimpin menjamin bahwa seluruh transaksi tulis yang telah di-commit sebelum pembacaan tiba **telah diterapkan 100% ke dalam mesin status penyimpanan**.
- Pembacaan lokal yang dieksekusi setelah langkah ini dijamin mengembalikan data paling mutakhir dan tidak pernah membaca data hantu atau basi.
Terbukti bahwa algoritma Read-Index memberikan garansi Linearizability penuh tanpa biaya penulisan I/O disk.
</details>

---

## 4. Bagian 3: Tantangan Live Coding & Triage Forensik (Production Implementation)

### Tantangan Implementasi: Simulator Mesin Status Konsensus Raft (Leader Election & Log Replication)
Sebagai Staff Distributed Systems Architect, implementasikan simulator inti algoritma konsensus Raft murni dalam Python dengan dukungan pemilihan pemimpin (*Leader Election*), replikasi log kuorum, penanganan heartbeat, dan ketahanan terhadap partisi jaringan buatan.

#### Spesifikasi Fungsional:
1. **Model Simpul Raft**: Setiap node mempertahankan status `FOLLOWER`, `CANDIDATE`, atau `LEADER`, serta variabel `current_term`, `voted_for`, dan `log` (list entri `{term, command}`).
2. **Mesin Pemilihan Suara (RequestVote)**: Kandidat meminta suara dari simpul lain; node hanya memberikan suara jika kandidat memiliki term lebih tinggi dan log yang minimal sama mutakhirnya (*Log Completeness Rule*).
3. **Replikasi Log & Komit Kuorum (AppendEntries)**: Pemimpin mereplikasi entri baru ke seluruh pengikut; entri dinyatakan `committed` jika telah diterima oleh mayoritas kuorum ($\lfloor N/2 \rfloor + 1$).
4. **Verifikasi Assert Eksekusi**: Mensimulasikan klaster 5 node, memvalidasi terpilihnya pemimpin tunggal, memutus 2 node ke dalam partisi minoritas, dan memastikan partisi mayoritas (3 node) tetap mampu memproses transaksi tanpa split-brain.

<details>
<summary><b>💻 Buka Solusi Arsitektur & Kode Produksi Standar Industri</b></summary>

```python
from dataclasses import dataclass, field

ROLE_FOLLOWER = "FOLLOWER"
ROLE_CANDIDATE = "CANDIDATE"
ROLE_LEADER = "LEADER"

@dataclass
class LogEntry:
    term: int
    command: str

class RaftNode:
    """
    Implementasi Simulator Mesin Status Konsensus Raft.
    """
    def __init__(self, node_id: int, peers: list[int]):
        self.node_id = node_id
        self.peers = peers # List ID node tetangga
        self.role = ROLE_FOLLOWER
        self.current_term = 0
        self.voted_for: int | None = None
        self.log: list[LogEntry] = []
        self.commit_index = -1
        self.last_applied = -1
        self.votes_received = 0

    def start_election(self):
        """Node beralih menjadi kandidat dan memulai pemilihan pemimpin."""
        self.role = ROLE_CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = 1 # Suara untuk diri sendiri

    def handle_request_vote(self, candidate_id: int, candidate_term: int, 
                            last_log_index: int, last_log_term: int) -> tuple[int, bool]:
        """
        Menangani pesan RPC RequestVote:
        Mengembalikan (current_term, vote_granted).
        """
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.role = ROLE_FOLLOWER
            self.voted_for = None

        vote_granted = False
        if candidate_term == self.current_term and (self.voted_for is None or self.voted_for == candidate_id):
            # Aturan Kelengkapan Log Raft:
            my_last_term = self.log[-1].term if self.log else 0
            my_last_index = len(self.log) - 1

            # Log kandidat minimal harus sama mutakhirnya dengan log lokal
            log_ok = (last_log_term > my_last_term) or \
                     (last_log_term == my_last_term and last_log_index >= my_last_index)

            if log_ok:
                vote_granted = True
                self.voted_for = candidate_id

        return self.current_term, vote_granted

    def handle_append_entries(self, leader_id: int, leader_term: int, 
                              prev_log_index: int, prev_log_term: int, 
                              entries: list[LogEntry], leader_commit: int) -> tuple[int, bool]:
        """
        Menangani pesan RPC AppendEntries (Heartbeat / Replikasi):
        Mengembalikan (current_term, success).
        """
        if leader_term > self.current_term:
            self.current_term = leader_term
            self.role = ROLE_FOLLOWER
            self.voted_for = None

        if leader_term < self.current_term:
            return self.current_term, False

        # Konfirmasi kepemimpinan sah
        self.role = ROLE_FOLLOWER

        # Verifikasi konsistensi log sebelumnya
        if prev_log_index >= 0:
            if prev_log_index >= len(self.log):
                return self.current_term, False
            if self.log[prev_log_index].term != prev_log_term:
                return self.current_term, False

        # Masukkan entri baru
        insert_idx = prev_log_index + 1
        for i, entry in enumerate(entries):
            idx = insert_idx + i
            if idx < len(self.log):
                self.log[idx] = entry
            else:
                self.log.append(entry)

        # Perbarui commit index
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)

        return self.current_term, True


class RaftClusterSimulator:
    """
    Simulator Jaringan Klaster Multi-Node Raft dengan kontrol partisi jaringan.
    """
    def __init__(self, node_ids: list[int]):
        self.nodes = {nid: RaftNode(nid, [p for p in node_ids if p != nid]) for nid in node_ids}
        self.isolated_nodes: set[int] = set()

    def isolate_node(self, node_id: int):
        self.isolated_nodes.add(node_id)

    def restore_node(self, node_id: int):
        self.isolated_nodes.discard(node_id)

    def trigger_election(self, candidate_id: int) -> bool:
        """Memicu pemilihan pada satu kandidat dan mengumpulkan suara kuorum."""
        candidate = self.nodes[candidate_id]
        if candidate_id in self.isolated_nodes:
            return False

        candidate.start_election()
        last_term = candidate.log[-1].term if candidate.log else 0
        last_idx = len(candidate.log) - 1

        for peer_id in candidate.peers:
            if peer_id in self.isolated_nodes:
                continue # Paket hilang akibat partisi jaringan

            peer = self.nodes[peer_id]
            _, granted = peer.handle_request_vote(
                candidate_id=candidate.node_id,
                candidate_term=candidate.current_term,
                last_log_index=last_idx,
                last_log_term=last_term
            )
            if granted:
                candidate.votes_received += 1

        quorum_needed = (len(self.nodes) // 2) + 1
        if candidate.votes_received >= quorum_needed:
            candidate.role = ROLE_LEADER
            return True
        return False

    def client_write(self, leader_id: int, command: str) -> bool:
        """Klien mengirimkan kueri tulis ke pemimpin."""
        leader = self.nodes[leader_id]
        if leader.role != ROLE_LEADER or leader_id in self.isolated_nodes:
            return False

        # Tambahkan ke log lokal pemimpin
        new_entry = LogEntry(term=leader.current_term, command=command)
        prev_idx = len(leader.log) - 1
        prev_term = leader.log[-1].term if leader.log else 0
        leader.log.append(new_entry)

        # Replikasi ke seluruh pengikut
        match_count = 1
        for peer_id in leader.peers:
            if peer_id in self.isolated_nodes:
                continue

            peer = self.nodes[peer_id]
            _, ok = peer.handle_append_entries(
                leader_id=leader.node_id,
                leader_term=leader.current_term,
                prev_log_index=prev_idx,
                prev_log_term=prev_term,
                entries=[new_entry],
                leader_commit=leader.commit_index
            )
            if ok:
                match_count += 1

        quorum_needed = (len(self.nodes) // 2) + 1
        if match_count >= quorum_needed:
            leader.commit_index = len(leader.log) - 1
            return True
        return False


# =====================================================================
# Unit Test & Verifikasi Pengujian Klaster Raft
# =====================================================================
if __name__ == "__main__":
    print("Memulai verifikasi mandiri Simulator Konsensus Raft...")

    # Buat klaster 5 node (Node 1 hingga 5, Kuorum = 3)
    cluster = RaftClusterSimulator(node_ids=[1, 2, 3, 4, 5])

    # 1. Uji Pemilihan Pemimpin (Election Test)
    # Node 1 mencalonkan diri menjadi pemimpin
    elected = cluster.trigger_election(candidate_id=1)
    print(f"Pemilihan Node 1: Terpilih={elected}, Role={cluster.nodes[1].role}")
    assert elected is True
    assert cluster.nodes[1].role == ROLE_LEADER
    assert cluster.nodes[1].votes_received == 5 # Mendapatkan seluruh 5 suara

    # 2. Uji Replikasi Log Konsensus
    # Klien menulis perintah "SET account_101 = 5000"
    success = cluster.client_write(leader_id=1, command="SET account_101 = 5000")
    print(f"Penulisan Transaksi 1: Berhasil={success}")
    assert success is True
    assert cluster.nodes[1].commit_index == 0
    # Verifikasi seluruh 4 pengikut memiliki entri log yang sama
    for nid in [2, 3, 4, 5]:
        assert len(cluster.nodes[nid].log) == 1
        assert cluster.nodes[nid].log[0].command == "SET account_101 = 5000"

    # 3. Uji Partisi Jaringan Minoritas (Toleransi 2 Node Crash)
    # Pisahkan Node 4 dan 5 ke dalam partisi terisolasi
    print("Mengisolasi Node 4 dan Node 5...")
    cluster.isolate_node(4)
    cluster.isolate_node(5)

    # Klaster kini memiliki 3 node aktif (Node 1, 2, 3). Kuorum mayoritas masih terpenuhi (3 >= 3)
    success_partitioned = cluster.client_write(leader_id=1, command="UPDATE account_101 += 250")
    print(f"Penulisan Transaksi 2 saat partisi minoritas: Berhasil={success_partitioned}")
    assert success_partitioned is True
    assert cluster.nodes[1].commit_index == 1

    # 4. Uji Penolakan Penulisan saat Kuorum Hilang (Partisi Mayoritas Putus)
    # Isolasi juga Node 3 (Kini tersisa hanya Node 1 dan 2 -> 2 node < kuorum 3)
    cluster.isolate_node(3)
    fail_partitioned = cluster.client_write(leader_id=1, command="UPDATE account_101 -= 1000")
    print(f"Penulisan Transaksi 3 saat kuorum hilang: Berhasil={fail_partitioned} (Ekspektasi: False)")
    assert fail_partitioned is False, "Sistem memperbolehkan penulisan tanpa kuorum mayoritas!"

    print("Pengujian konsensus Raft Multi-Node lolos 100% tanpa kesalahan konsistensi!")
```
</details>

---

## 5. Rubrik Evaluasi Mandiri L6 Staff & Peta Remediasi

| Tingkat Pencapaian | Klasifikasi Kemahiran | Rekomendasi Remediasi Terfokus |
|---|---|---|
| **0% – 50%** | **Below Staff Target** | Ulas kembali pola arsitektur server backend dan sistem terdistribusi dasar pada [Modul 149: Arsitektur Server HTTP & Pemodelan API](../curriculum/09-software-engineering-cloud-sre/149-back-end-arsitektur-server-http-api.md) dan [Modul 153: Keandalan & Ketahanan Sistem Terdistribusi](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md). |
| **51% – 75%** | **Borderline L5/Senior** | Perdalam transaksi ACID dan basis data terdistribusi pada [Modul 162: Transaksi ACID & Kontrol Konkurensi Lanjut](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md) dan [Modul 164: Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md). |
| **76% – 90%** | **Strong Staff L6** | Kuasai orkestrasi internal Kubernetes dan rekayasa data massal pada [Modul 155: Orkestrasi Kontainer & Bedah Internal Kubernetes](../curriculum/09-software-engineering-cloud-sre/155-orkestrasi-kontainer-bedah-internal-kubernetes.md) dan [Modul 165: Data Engineering & Pemrosesan Data Massal](../curriculum/10-basis-data-enterprise/165-data-engineering-pemrosesan-data-massal.md). |
| **91% – 100%** | **Distinguished / Principal (L7+)** | Siap memimpin arsitektur komputasi awan global dan basis data terdistribusi multi-wilayah. Pelajari panduan karier lengkap pada [`track-distributed-systems-cloud-architect.md`](../tracks/track-distributed-systems-cloud-architect.md). |

### Peta Remediasi Modul Terkait:
- Modul 143: [Arsitektur Perangkat Lunak Skala Besar](../curriculum/09-software-engineering-cloud-sre/143-arsitektur-perangkat-lunak-skala-besar.md)
- Modul 152: [Pemrosesan Pesan Asinkron & Event-Driven](../curriculum/09-software-engineering-cloud-sre/152-back-end-pemrosesan-pesan-asinkron.md)
- Modul 153: [Keandalan & Ketahanan Sistem Terdistribusi](../curriculum/09-software-engineering-cloud-sre/153-sistem-terdistribusi-keandalan-ketahanan.md)
- Modul 155: [Orkestrasi Kontainer & Bedah Internal Kubernetes](../curriculum/09-software-engineering-cloud-sre/155-orkestrasi-kontainer-bedah-internal-kubernetes.md)
- Modul 156: [Tiga Pilar Observabilitas & Rekayasa SRE](../curriculum/09-software-engineering-cloud-sre/156-observabilitas-tiga-pilar-sre.md)
- Modul 160: [Arsitektur Internal Mesin Penyimpanan](../curriculum/10-basis-data-enterprise/160-arsitektur-internal-mesin-penyimpanan-basis-data.md)
- Modul 162: [Transaksi ACID & Kontrol Konkurensi Lanjut](../curriculum/10-basis-data-enterprise/162-transaksi-acid-kontrol-konkurensi-lanjut.md)
- Modul 164: [Basis Data Terdistribusi & Konsensus Global](../curriculum/10-basis-data-enterprise/164-basis-data-terdistribusi-konsensus-global.md)
- Trek Karier: [`track-distributed-systems-cloud-architect.md`](../tracks/track-distributed-systems-cloud-architect.md)
- Spaced Repetition: [`deck-07-dsp-networking-distributed-systems.md`](../flashcards/deck-07-dsp-networking-distributed-systems.md)
