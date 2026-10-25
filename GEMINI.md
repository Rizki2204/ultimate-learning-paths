# Aturan Utama Kurikulum Ultimate Learning Paths: Standar Pedagogi "Dari Nol Mutlak (Bayi Baru Lahir) hingga Mahir 100%"

Setiap materi pembelajaran di dalam repositori ini WAJIB ditulis sebagai **Bimbingan Mentor & Tutorial Interaktif dari Titik Nol Mutlak**, BUKAN seperti dokumentasi kaku, kamus rumus, atau jurnal akademis yang membuat pusing.

## 1. Prinsip Emas: Anggap Pembaca Mulai dari 0 Mutlak (Seperti Bayi Baru Lahir)
1. **Dilarang Keras Langsung Melempar Jargon atau Rumus (*Zero-Notation Shock*)**:
   - Jangan pernah menggunakan istilah teknis (seperti *vektor, matriks, pivot, ortogonal, determinan, nilai eigen, tensor*) atau simbol matematika ($\sum, \prod, \in, \forall, \mathbb{R}^n, A^T$) tanpa terlebih dahulu menjelaskan:
     - **Apa itu dalam bahasa sehari-hari yang paling sederhana?** (Contoh: belanja paket makanan di warung, arah jalan kaki di ubin lantai, mencampur cat air, senter & bayangan, menarik adonan martabak).
     - **Bagaimana cara membacanya secara lisan dalam bahasa manusia?** (Contoh: *"Simbol $\mathbf{x} \in \mathbb{R}^3$ dibaca: $x$ adalah daftar berisi 3 angka biasa"*).
     - **Kenapa kita butuh benda/konsep ini?** Masalah nyata apa yang ribet kalau tidak pakai konsep ini?
2. **Gaya Bahasa Mentor yang Hangat, Mengalir & Membimbing**:
   - Gunakan bahasa Indonesia yang santai namun jelas dan terstruktur, seolah-olah seorang kakak/mentor ahli sedang mengajari secara tatap muka dari nol sampai benar-benar paham (*"Yuk kita bedah pelan-pelan...", "Jangan panik lihat simbol ini, artinya sebenarnya cuma...", "Coba bayangkan..."*).
3. **Tangga Belajar Bertahap 7-Level (Gradual Scaffolding — Jangan Melompat!)**:
   - **Level 0 (Konsep Bayi / Dunia Nyata & Pengantar Pra-Materi)**: Penjelasan 100% tanpa rumus, murni cerita/ilustrasi sehari-hari dan logika akal sehat. Jika bab membutuhkan konsep dasar yang belum pernah muncul di topik sebelumnya (termasuk jembatan indeks 1-based Matematika vs 0-based Python dan cara dasar membaca kode Python), wajib buka dengan **Pengantar Pra-Materi dari Nol**.
   - **Level 1 (Kenalan dengan Angka Kecil $2 \times 2$ & Kamus Simbol Anti-Pusing)**: Mulai pakai angka super kecil (1, 2, 3) pada ukuran terkecil ($2 \times 2$) dan visualisasi sederhana, disertai kotak terjemahan simbol ke bahasa manusia.
   - **Level 2 (Tutorial Resep Langkah-demi-Langkah & Tanya-Jawab Pemula)**: Panduan tutorial *step-by-step* lengkap dengan alasan di balik setiap langkah (*"Kenapa baris 2 dikurangi 2 kali baris 1? Karena..."*) dan kotak *"❓ Pertanyaan Pemula: Kok bisa begitu?"*.
   - **Level 3 (Tips, Trik, Rahasia Cepat Paham & Jembatan Keledai)**: Kotak khusus berisi trik praktis, jembatan keledai (misal *BASKOM = Baris-Kolom*), pola rahasia, dan cara cek jawaban sendiri dalam 5 detik.
   - **Level 4 (Rumus Formal & Pembuktian Terpandu dengan Jembatan Logika)**: Pertahankan 100% kedalaman universitas kelas dunia (MIT 18.06/18.065, Strang, Kolda & Bader), namun setiap baris penurunan rumus wajib didampingi **Jembatan Logika Baris-demi-Baris** (*"Dari baris 1 ke baris 2 kita cuma melakukan..."*).
   - **Level 5 (Tutorial Koding Python 2-Tahap dari Nol + Eksperimen 60 Detik)**:
     - **Tahap 5A (Kode Mainan Pure Python Tanpa Library)**: Tunjukkan logika dasarnya menggunakan `list` dan `for` loop Python murni pada angka kecil agar pemula yang belum pernah memakai `numpy` paham apa yang sebenarnya dikerjakan komputer.
     - **Tahap 5B (Kode Standar Industri NumPy/SciPy + Tabel Bedah Baris-demi-Baris + Output ` ```text `)**: Kode produksi lengkap diikuti blok output ` ```text `, **Tabel Bedah Kode Baris-demi-Baris** (`| Baris Kode | Apa yang Dilakukan Komputer | Terjemahan Bahasa Manusia |`), serta kotak **"🔬 Eksperimen Mandiri 60 Detik (Ubah 1 Angka & Amati!)"**.
   - **Level 6 (Jebakan Pemula, Kisah Nyata Industri & Latihan 4 Jenjang)**: Kesalahan umum pemula + solusinya, studi kasus industri, dan latihan mandiri bertahap (**Tingkat 1: Pemanasan Bayi / Hitung Jari $\to$ Tingkat 2: Pemula / Tulis Tangan $\to$ Tingkat 3: Menengah / Pemodelan & Koding $\to$ Tingkat 4: Mahir / Tantangan Industri**) lengkap dengan pembahasan di dalam tag `<details>`.

## 2. Daftar Wajib & Guardrail Teknis di Setiap Bab Subtopik
1. **Kotak "Kamus Simbol Anti-Pusing" & "Jembatan Logika" (Aturan Anti-Bentrok Heading)**:
   - Karena skrip `verify_pilot_011.py` melarang adanya judul `##`/`###`/`####` yang kembar di dalam satu file yang sama, gunakan **Blockquote Callout** (`> **🔤 Kamus Simbol Anti-Pusing — [Nama Rumus]:**`) atau sertakan nama unik rumus pada subjudul (`#### 🔤 Kamus Simbol Anti-Pusing: [Nama Rumus Unik]`).
2. **Kotak "Micro-Primer Mandiri" untuk Konsep Lintas Topik (Larangan Forward-Reference Buta)**:
   - Dilarang menggunakan konsep dari topik kurikulum yang nomor urutnya lebih tinggi (misal: Python dasar dari Tingkat 5/6, rata-rata/varians/kovarians dari Topik 017, pengali Lagrange/turunan parsial dari Topik 014, bilangan kompleks dari Topik 016, atau floating-point underflow dari Topik 021) tanpa menyediakan **Kotak Micro-Primer Mandiri dari Nol** tepat di tempat konsep tersebut pertama kali dipakai.
3. **Aturan Blok Kode Python Mandiri (Self-Contained Runnable Blocks) & Bebas Karakter Kontrol Rusak**:
   - Setiap blok ```` ```python ```` dieksekusi di dalam proses terpisah (*isolated subprocess*). Pastikan setiap blok kode mandiri 100% (memiliki `import` dan variabelnya sendiri).
   - Pastikan tidak ada karakter kontrol ASCII rusak (`\x07`, `\x08`, atau tab/newline tidak sengaja akibat `\alpha`, `\beta`, `\text`, `\neq`) di dalam rumus LaTeX maupun string kode.
4. **Kejujuran Label Tautan, Visualisasi Interaktif & Sinkronisasi Ekosistem 1:1**:
   - Sertakan tautan langsung (*deep links*) aktif (`HTTP 200 OK`) ke sumber belajar & visualisasi interaktif terbaik (3Blue1Brown, MIT OCW, Immersive Linear Algebra, Georgia Tech ILA, Setosa Visually Explained) dengan label yang 100% jujur dan panduan tonton/baca bagi pemula.
   - Setiap bab subtopik wajib memiliki latihan pendamping di `drills/` (dengan *Petunjuk Bertahap* dan *Solusi Lengkap*) serta kartu di kedua format `flashcards/` (`.md` dan `.tsv` yang tersinkronisasi 1:1).
