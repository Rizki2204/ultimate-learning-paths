# Master Portal Spaced-Repetition Active Recall Decks (`flashcards/`)

Selamat datang di repositori flashcards spaced-repetition resmi `ultimate-learning-paths`.
Repositori ini dirancang untuk melengkapi studi kurikulum modular 17 tingkat melalui retensi memori jangka panjang berbasis sains kognitif.

## Metodologi Sains Kognitif & Algoritma Spaced Repetition

### 1. Kurva Melupakan Ebbinghaus (Ebbinghaus Forgetting Curve)
Secara empiris, memori manusia atas informasi baru mengalami penurunan eksponensial seiring waktu:
$$R = e^{-\frac{t}{S}}$$
di mana $R$ adalah retensi memori, $t$ adalah interval waktu sejak review terakhir, dan $S$ adalah kekuatan memori (*memory stability*). Ulasan aktif (*active recall*) terjadwal secara berkala mereset kurva peluruhan dan meningkatkan stabilitas memori $S$ secara signifikan.

### 2. Rekomendasi Algoritma Penjadwalan: FSRS vs SM-2
- **FSRS (Free Spaced Repetition Scheduler)**: Sangat direkomendasikan. FSRS adalah algoritma berbasis machine learning modern yang memodelkan DSR (*Difficulty, Stability, Retrievability*). FSRS mengoptimalkan jadwal review dengan akurasi 20-30% lebih tinggi dibanding algoritma berbasis heuristik SM-2.
  - **Target Retention**: Atur pada rentang `0.85` hingga `0.90` (85%-90%). Angka ini merupakan sweet-spot efisiensi waktu vs retensi.
  - **Maximum Interval**: 365 hari (1 tahun).
- **SM-2 (SuperMemo 2)**: Algoritma klasik default Anki. Jika menggunakan SM-2, pertahankan Ease Factor awal di 250%, Interval Modifier 100%, dan Learning Steps `15m 1d 3d`.

---

## Panduan Impor ke Anki (Langkah-demi-Langkah)

Setiap deck dalam direktori ini tersedia dalam dua format yang saling berpasangan:
1. **`.tsv` (Tab-Separated Values)**: Berkas data murni yang siap diimpor ke aplikasi [Anki](https://apps.ankiweb.net/).
2. **`.md` (Markdown Companion)**: Dokumentasi lengkap yang dapat dibaca dan dicari secara visual di browser, Obsidian, atau VS Code.

### Langkah Impor File `.tsv` ke Anki:
1. Buka aplikasi **Anki Desktop** (versi 2.1.55+ direkomendasikan).
2. Klik menu **File** -> **Import...** (atau shortcut `Ctrl+I` / `Cmd+I`).
3. Pilih salah satu file `.tsv` dari direktori `flashcards/` (misalnya `deck-01-cognitive-logic-math.tsv`).
4. Pada jendela dialog impor:
   - **Type (Tipe Catatan)**: Pilih **Cloze**.
   - **Deck**: Pilih atau buat deck tujuan (misal `Ultimate::Deck-01-Cognitive-Logic-Math`).
   - **Field separator**: Pilih **Tab**.
   - **Allow HTML in fields**: Centang kotak (**Yes**).
   - **Field mapping**:
     - Kolom 1 (Text) -> Field `Text`
     - Kolom 2 (Extra) -> Field `Extra`
     - Kolom 3 (Tags) -> Pilih opsi **Tags** di pojok kanan bawah Anki.
5. Klik tombol **Import**. Kartu akan masuk ke profil Anki Anda dengan seluruh cloze deletions siap diuji.

---

## Inventaris 10 Deck Spaced-Repetition

| No | Deck ID | Berkas TSV | Berkas Markdown | Jml Kartu | Tingkat Terkait | Domain Inti |
|---|---|---|---|---|---|---|
| 01 | `deck-01-cognitive-logic-math` | [`deck-01-cognitive-logic-math.tsv`](./deck-01-cognitive-logic-math.tsv) | [`deck-01-cognitive-logic-math.md`](./deck-01-cognitive-logic-math.md) | 25 | Tingkat 0, Tingkat 1 | Fondasi Kognitif, Logika Murni & Matematika Komprehensif |
| 02 | `deck-02-physics-circuits-semiconductors` | [`deck-02-physics-circuits-semiconductors.tsv`](./deck-02-physics-circuits-semiconductors.tsv) | [`deck-02-physics-circuits-semiconductors.md`](./deck-02-physics-circuits-semiconductors.md) | 25 | Tingkat 2, Tingkat 3 | Fisika Semikonduktor, Rangkaian Listrik & Mikroelektronika |
| 03 | `deck-03-digital-logic-computer-architecture` | [`deck-03-digital-logic-computer-architecture.tsv`](./deck-03-digital-logic-computer-architecture.tsv) | [`deck-03-digital-logic-computer-architecture.md`](./deck-03-digital-logic-computer-architecture.md) | 25 | Tingkat 4 | Logika Digital, Computer Engineering & Arsitektur Komputer |
| 04 | `deck-04-embedded-rtos-firmware` | [`deck-04-embedded-rtos-firmware.tsv`](./deck-04-embedded-rtos-firmware.tsv) | [`deck-04-embedded-rtos-firmware.md`](./deck-04-embedded-rtos-firmware.md) | 25 | Tingkat 5 | Embedded Systems, Firmware Bare-Metal & RTOS / IoT |
| 05 | `deck-05-dsa-compilers-pl` | [`deck-05-dsa-compilers-pl.tsv`](./deck-05-dsa-compilers-pl.tsv) | [`deck-05-dsa-compilers-pl.md`](./deck-05-dsa-compilers-pl.md) | 25 | Tingkat 6 | Computer Science Core, Algoritma, Teori Bahasa & Rekayasa Kompiler |
| 06 | `deck-06-os-internals-linux-kernel` | [`deck-06-os-internals-linux-kernel.tsv`](./deck-06-os-internals-linux-kernel.tsv) | [`deck-06-os-internals-linux-kernel.md`](./deck-06-os-internals-linux-kernel.md) | 25 | Tingkat 7 | Operating Systems Internals & Rekayasa Linux Kernel |
| 07 | `deck-07-dsp-networking-distributed-systems` | [`deck-07-dsp-networking-distributed-systems.tsv`](./deck-07-dsp-networking-distributed-systems.tsv) | [`deck-07-dsp-networking-distributed-systems.md`](./deck-07-dsp-networking-distributed-systems.md) | 25 | Tingkat 8, Tingkat 9, Tingkat 10 | Pemrosesan Sinyal, Jaringan Komputer & Sistem Terdistribusi |
| 08 | `deck-08-cybersecurity-cryptography-pwn` | [`deck-08-cybersecurity-cryptography-pwn.tsv`](./deck-08-cybersecurity-cryptography-pwn.tsv) | [`deck-08-cybersecurity-cryptography-pwn.md`](./deck-08-cybersecurity-cryptography-pwn.md) | 25 | Tingkat 11 | Keamanan Siber, Kriptografi Matematika & Rekayasa Eksploitasi Binary |
| 09 | `deck-09-ai-deep-learning-cuda-nlp` | [`deck-09-ai-deep-learning-cuda-nlp.tsv`](./deck-09-ai-deep-learning-cuda-nlp.tsv) | [`deck-09-ai-deep-learning-cuda-nlp.md`](./deck-09-ai-deep-learning-cuda-nlp.md) | 25 | Tingkat 12, Tingkat 13 | Data Science, Deep Learning, Komputasi CUDA GPU & Pemrosesan Bahasa Alami |
| 10 | `deck-10-fintech-hft-robotics-hpc` | [`deck-10-fintech-hft-robotics-hpc.tsv`](./deck-10-fintech-hft-robotics-hpc.tsv) | [`deck-10-fintech-hft-robotics-hpc.md`](./deck-10-fintech-hft-robotics-hpc.md) | 25 | Tingkat 14, Tingkat 15, Tingkat 16 | Fintech, Perdagangan Berfrekuensi Tinggi, Robotika & Superkomputasi |

**Total Kartu Keseluruhan**: 250 kartu spesifikasi tinggi.

---

## 5 Kategori Pengetahuan Wajib yang Dicakup
Setiap deck mencakup 5 pilar pengetahuan rekayasa standar emas:
1. **Foundational Definitions**: Definisi formal, aksioma matematika, dan sifat fundamental.
2. **Mathematical Identities**: Teorema kunci, penurunan kalkulus/aljabar, formula performa asimtotik.
3. **Architecture Constants**: Angka latensi perangkat keras nyata, ukuran cache line, page frames, dan batas register.
4. **Assembly Opcodes & Byte Layouts**: Opcode mesin biner (RISC-V, ARM Thumb-2, x86_64, NVIDIA PTX), bit fields, dan vektor interupsi.
5. **Design Heuristics & Rules of Thumb**: Aturan praktis industri, pola perancangan non-blocking, eliminasi jitter, dan pemulihan kegagalan.

---

## Contoh Struktur Kartu Cloze Anki
```text
Text:   Aturan inferensi logika yang menyatakan jika {{c1::P -> Q}} dan {{c1::P}} benar maka {{c2::Q}} benar dinamakan {{c2::Modus Ponens}}.
Extra:  Modus Ponens merupakan dasar deduksi matematika klasik: ((P -> Q) /\ P) |= Q.
Tags:   tier-00::logika logic::deduction foundational-definitions
```
