# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 00 (Topics 1-5):
Fondasi Kognitif, Logika Murni & Berpikir Ilmiah.
"""

DATA_TIER_00 = {
    1: {
        "trace": """#### Tabel Penelusuran Transisi Kognitif & Konsolidasi Memori (Spaced Repetition)
| Langkah / Tahap Kognitif | Komponen / Struktur Mental | Input / Bukti Empiris | Operasi Logika & Transisi State | Status Representasi / Memori | Status Output / Kesimpulan Valid |
|---|---|---|---|---|---|
| Inisialisasi T+0 | Encoding Awal | Konsep baru diterima panca indra | Pembentukan jejak memori awal via sinapsis hipokampus | $R(0) = 1.0, S = 1.0$ (Stabilitas awal) | Pemahaman awal terbentuk pada memori kerja |
| Hari T+1 (Uji 1) | Pembusukan Ebbinghaus | $t = 1\\text{ hari}$, tanpa recall | Evaluasi kurva retensi: $R(1) = e^{-1/1} \\approx 0.368$ | Memori memudar, batas ambang recall terancam | Sinyal peringatan: perlu intervensi aktif recall |
| Hari T+1 (Recall) | Feynman Active Retrieval | Pertanyaan diagnostik tanpa melihat catatan | Rekonstruksi mandiri konsep dalam analogi sederhana | Lonjakan stabilitas: $S_{new} = S \\cdot (1 + a \\cdot e^{-b R})$ | Penguatan Long-Term Potentiation (LTP) sinaptik |
| Hari T+3 (Uji 2) | Spaced Interval Expansion | $t = 3\\text{ hari}$ pasca review 1 | Evaluasi interval eksponensial baru: $I_2 = I_1 \\cdot EF$ | $R(3) \\ge 0.88, S = 4.2$ | Retensi stabil, transfer ke neokorteks jangka panjang |
| Hari T+7 (Audit) | Metakognisi & Kalibrasi | Uji transfer pada domain masalah baru | Identifikasi blind spot penalaran (*illusion of explanatory depth*) | Peta mental terkalibrasi tanpa ilusi kompetensi | Penguasaan konsep terverifikasi secara empiris |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Falsifikasi Lobotomi Medis Walter Freeman (1940-an)",
            "chronology": """- **Kronologi & Konteks Sejarah**: Antara tahun 1936 hingga 1967, ahli saraf Walter Freeman melakukan sekitar 3.500 prosedur lobotomi transorbital (*icepick lobotomy*) di Amerika Serikat. Freeman mengklaim teknik ini menyembuhkan penyakit mental berat dengan memutuskan serat lobus frontal.
- **Akar Masalah Kognitif**: Freeman mengalami bias konfirmasi ekstrem (*confirmation bias*) dan ketiadaan metodologi falsifikasi. Pasien yang menjadi apatis, kehilangan kepribadian, atau vegetatif dilabeli sebagai 'sembuh dan tenang'. Tidak pernah ada uji klinis terkontrol acak (RCT) atau kelompok kontrol independen, mengacaukan pembiusan pasif dengan perbaikan kognitif riil.""",
            "snippet": """```python
# Simulasi Ebbinghaus Decay vs Spaced Repetition Memory Scheduling (SM-2 Model)
import math

class MemoryItem:
    def __init__(self, concept_name: str):
        self.concept_name = concept_name
        self.stability = 1.0  # Hari sebelum retensi drop ke 90%
        self.easiness_factor = 2.5
        self.repetition = 0

    def recall_probability(self, days_elapsed: float) -> float:
        # Kurva pembusukan Ebbinghaus: R(t) = exp(-t / S)
        return math.exp(-days_elapsed / self.stability)

    def review_feedback(self, grade: int):
        # Algoritma SuperMemo SM-2 asli untuk mitigasi ilusi kompetensi
        # grade: 0 (lupa total) s/d 5 (ingat sempurna tanpa ragu)
        assert 0 <= grade <= 5, "Grade harus bernilai 0..5"
        if grade >= 3:
            if self.repetition == 0:
                interval = 1.0
            elif self.repetition == 1:
                interval = 6.0
            else:
                interval = self.stability * self.easiness_factor
            self.repetition += 1
            self.stability = interval
        else:
            self.repetition = 0
            self.stability = 1.0

        # Update easiness factor
        self.easiness_factor = max(1.3, self.easiness_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02)))
```""",
            "analysis": """- **Analisis Epistemologis & Rekayasa Modern**: Tragedi Freeman mendasari standar ganda kedokteran modern: pembuktian ilmiah memerlukan hipotesis nol ($H_0$), eksperimen buta ganda (*double-blind*), dan metrik evaluasi objektif pra-eksperimen. Pada rekayasa perangkat lunak, bias ini setara dengan 'happy path testing'—mengasumsikan sistem andal hanya karena tidak melempar crash pada satu skenario sukses."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Rancang program CLI pembelajaran aktif yang mengimplementasikan algoritma spaced repetition SuperMemo SM-2 untuk melacak retensi memori 10 kartu konsep.
- **Petunjuk Perancangan Arsitektur**:
  - Buat kelas `Flashcard` yang menyimpan parameter `repetition_count`, `easiness_factor` (default 2.5), dan `interval_days`.
  - Terapkan fungsi transisi state saat menerima skor metakognitif (0-5) dari pengguna.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: Skor berturut-turut `[5, 4, 5]`.
  - *Keluaran yang Diharapkan*: `interval_days` berkembang dari `1` $\\to$ `6` $\\to$ `14.4` hari, `easiness_factor` $\\ge 2.5$.
  - *Kasus Batas (Edge Case)*: Skor `0` (lupa total) setelah interval 60 hari. Interval wajib ter-reset ke `1.0` hari dan pengulangan kembali ke `0`.
- **Rubrik Penilaian Mandiri**: 40% Formula SM-2 Eksak Bebas Bug, 30% Penanganan Reset Interval pada Kegagalan Recall, 30% Kemandirian Kode Python Standard Library.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan simulator simulasi kognitif yang membandingkan retensi 1.000 mahasiswa yang belajar via *massed practice* (cramming semalam) vs *distributed practice* (spaced repetition) selama rentang 180 hari.
- **Petunjuk Perancangan Arsitektur**:
  - Simulasikan pembusukan eksponensial $R(t) = e^{-t/S}$ harian untuk setiap konsep.
  - Tambahkan derau Gaussian $\\mathcal{N}(0, 0.05)$ pada stabilitas untuk merefleksikan variabilitas biologis individu.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Beban*: 1.000 agen dengan 50 materi belajar selama 180 tick harian.
  - *Keluaran yang Diharapkan*: Pada hari ke-180, kelompok cramming memiliki rerata retensi $< 15\\%$, kelompok spaced repetition mempertahankan retensi $> 80\\%$.
  - *Kasus Batas*: Agen dengan tingkat lupa tinggi ($S_{base} = 0.5$); algoritma harus meningkatkan frekuensi pengulangan secara adaptif tanpa overflow loop.
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Pemodelan Diferensial Retensi, 30% Kestabilan Komputasi Matriks NumPy, 30% Visualisasi Kurva Retensi Bersih.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin penalaran Feynman Technique yang memvalidasi penjelasan teknis terhadap pendeteksian jargon lingkaran (*circular definition detector*) menggunakan representasi graf konsep berarah (DAG).
- **Petunjuk Perancangan Arsitektur**:
  - Urai teks penjelasan menjadi graf ketergantungan semantik simpul-konsep.
  - Terapkan deteksi siklus Tarjan's Strongly Connected Components untuk mengidentifikasi apakah konsep $A$ dijelaskan menggunakan $B$ yang didefinisikan kembali via $A$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Uji*: Teks dengan definisi melingkar: *"Enkripsi adalah proses kriptografi yang mengamankan data dengan algoritma enkripsi"*.
  - *Keluaran yang Diharapkan*: Sistem mendeteksi siklus dependensi tertutup dan menolak penjelasan dengan mengembalikan path simpul yang berputar.
  - *Kasus Batas*: Input graf asiklik murni berkedalaman 20 lapis; sistem harus memvalidasi bahwa seluruh daun (*leaf nodes*) merujuk pada prinsip pertama dasar tanpa siklus.
- **Rubrik Penilaian Mandiri**: 40% Ketepatan Deteksi Siklus Graf Topological, 30% Ekstraksi Ketergantungan Entitas Bersih, 30% Dokumentasi Algoritma Deteksi Formal."""
    },
    2: {
        "trace": """#### Tabel Penelusuran Dekonstruksi Masalah (First-Principles Thinking)
| Langkah / Tahap Kognitif | Komponen / Struktur Mental | Input / Bukti Empiris | Operasi Logika & Transisi State | Status Representasi / Memori | Status Output / Kesimpulan Valid |
|---|---|---|---|---|---|
| Langkah 0: Dogma | Analogy Heuristic | "Paket baterai EV berharga $600/kWh dari supplier" | Menerima premis konvensional tanpa dekomposisi | Model mental bias pasar modal industri otomotif | Kesimpulan palsu: Mobil listrik mustahil murah |
| Langkah 1: Skeptisisme | Reduksi Premis | Harga pasar vs komposisi material | Pemisahan mark-up rantai pasok dari biaya fisika murni | Premis pasar dibatalkan | Fokus dialihkan ke tabel periodik unsur |
| Langkah 2: Dekonstruksi | Analisis Material | Logam spot LME: Nikel, Kobalt, Litium, Aluminium | Perhitungan massa atom dan stoikiometri per kWh energi | Berat per kWh: 0.8 kg Li, 4.5 kg Ni, 1.2 kg Co | Biaya bahan baku murni: ~$80/kWh |
| Langkah 3: Rekonstruksi | Sintesis Struktur | 6.831 sel komoditas laptop 18650 standar industri | Integrasi sel kecil dengan sirkulasi pendingin cair | Desain baterai modular terisolasi termal | Kelayakan termal dan proteksi runaway terbukti |
| Langkah 4: Validasi | Uji Prinsip Pertama | Estimasi pabrikasi skala Gigafactory | $C_{total} = C_{materials} + C_{energy} + C_{overhead}$ | Biaya riil: ~$110/kWh | Paradigma industri bergeser secara revolusioner |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Bencana Rantai Pasok Baterai Kendaraan Listrik GM EV1 & Dekonstruksi First-Principles (1996)",
            "chronology": """- **Kronologi & Konteks Sejarah**: Pada 1996, General Motors meluncurkan EV1, mobil listrik komersial pertama era modern. Namun pada 2003, GM membatalkan seluruh program, menarik seluruh unit dari konsumen, dan menghancurkannya di gurun Arizona.
- **Akar Masalah Penalaran**: Manajemen GM bernalar berdasarkan analogi (*reasoning by analogy*): mereka mengasumsikan baterai asam-timbal dan NiMH harus dibeli dalam paket besar kustom dari vendor baterai militer/kedirgantaraan seharga $600+/kWh, menyimpulkan bahwa EV tidak akan pernah ekonomis. Tesla menolak analogi ini pada 2004, mendekonstruksi baterai ke tingkat harga spot unsur logam dasar di London Metal Exchange ($80/kWh), lalu merakit ribuan sel laptop silinder standar 18650.""",
            "snippet": """```python
# Analisis Biaya Prinsip Pertama vs Penalaran Analogi Konvensional
class FirstPrinciplesCostEngine:
    def __init__(self):
        # Harga spot komoditas pasar logam dasar (USD per kg)
        self.raw_material_spot_prices = {
            "lithium_carbonate": 16.5,  # USD/kg
            "nickel_class1": 18.2,       # USD/kg
            "cobalt": 32.0,              # USD/kg
            "aluminum": 2.4,             # USD/kg
            "copper": 8.8                # USD/kg
        }

    def compute_material_floor_cost(self, kwh_capacity: float, chemistry_weights: dict) -> float:
        # Menghitung batas bawah fisik biaya material (Physical Cost Floor)
        total_material_cost = 0.0
        for element, kg_per_kwh in chemistry_weights.items():
            price_per_kg = self.raw_material_spot_prices.get(element, 0.0)
            total_material_cost += kg_per_kwh * price_per_kg * kwh_capacity
        return total_material_cost

    def evaluate_assembly_efficiency(self, floor_cost: float, vendor_quote: float) -> float:
        # Rasio inefisiensi rantai pasok analogi vs prinsip pertama
        assert floor_cost > 0, "Batas bawah biaya material harus positif"
        return vendor_quote / floor_cost

# Bobot material per kWh baterai NMC-811
nmc811_kg_per_kwh = {
    "lithium_carbonate": 0.85,
    "nickel_class1": 4.10,
    "cobalt": 0.52,
    "aluminum": 1.80,
    "copper": 1.25
}
engine = FirstPrinciplesCostEngine()
floor = engine.compute_material_floor_cost(100.0, nmc811_kg_per_kwh)
# Floor cost ~ $10,500 untuk 100 kWh ($105/kWh) vs kutipan analogi $600/kWh ($60,000)
```""",
            "analysis": """- **Analisis Forensik & Rekayasa Modern**: Kegagalan GM EV1 adalah kegagalan kognitif paradigma analogi. Dalam rekayasa perangkat lunak, jebakan serupa terjadi ketika arsitek memilih arsitektur 'karena Google atau Netflix menggunakannya' tanpa membedah apakah kendala matematis beban jaringan mereka sama. Berpikir dari prinsip pertama menuntut reduksi ke batasan termodinamika dan kompleksitas komputasional murni."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Buat program dekonstruksi pohon biaya rekursif yang memecah biaya komponen perangkat lunak/keras ke level atomik material/sumber daya terendah.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun kelas `ComponentNode` dengan struktur pohon hierarkis (`children`).
  - Simpul daun (*leaf*) merepresentasikan elemen tak tereduksi (material fisik dasar, jam komputasi CPU, atau bandwidth jaringan).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: Pohon 3-tingkat modul penyimpanan SSD (NAND Flash $\\to$ Silikon Wafer, Controller $\\to$ PCB Tembaga).
  - *Keluaran yang Diharapkan*: Perhitungan batas bawah biaya agregat dari bawah ke atas (*bottom-up physical floor*).
  - *Kasus Batas*: Siklus rekursif dalam dependensi anak; program harus memvalidasi invariant DAG dan melempar `ValueError` bila ada siklus.
- **Rubrik Penilaian Mandiri**: 40% Rekursi Bottom-Up Akurat, 30% Validasi Invariant DAG Anti-Siklus, 30% Struktur Kelas Bersih dan Modular.

### Tingkat 2: Menengah
- **Tugas**: Bangun mesin optimasi komputasi yang mengevaluasi apakah suatu fungsi aljabar lambat dapat didekonstruksi dari pemanggilan pustaka umum ke operasi bitwise / lookup table prinsip pertama.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan algoritma Fast Inverse Square Root (`0x5f3759df`) vs `1.0 / math.sqrt(x)`.
  - Ukur siklus instruksi CPU rata-rata dan galat relatif presisi IEEE-754.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Vektor Uji*: $x \\in [0.001, 100000.0]$ dengan 10.000 sampel acak.
  - *Keluaran yang Diharapkan*: Galat relatif $\\le 0.175\\%$, kecepatan eksekusi meningkat drastis pada arsitektur target.
  - *Kasus Batas*: $x \\le 0$ atau $x = \\text{NaN}$; fungsi wajib menangani representasi denormalized float tanpa crash hardware trap.
- **Rubrik Penilaian Mandiri**: 40% Dekonstruksi Bitwise IEEE-754 Benar, 30% Analisis Galat Komparatif Rigor, 30% Benchmark Waktu Eksekusi Terisolasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang sistem penilai arsitektur sistem terdistribusi yang memverifikasi apakah klaim throughput transaksi didukung oleh batasan fisik perangkat keras (hukum batas bandwidth I/O PCIe, kecepatan cahaya kabel serat optik, dan latensi DRAM).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan batasan fisik dasar: $c \\approx 200\\text{ km/ms}$ dalam serat optik, latensi akses DRAM $\\approx 60\\text{ ns}$, bandwidth bus NVMe $\\approx 7\\text{ GB/s}$.
  - Evaluasi proposal sistem: tolak arsitektur terdistribusi lintas-benua yang mengklaim latensi konsensus $< 5\\text{ ms}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kasus Pelanggaran*: Klaim Raft konsensus 3 data center (New York, London, Tokyo) dengan latensi commit 2 ms.
  - *Keluaran yang Diharapkan*: Sistem memvalidasi pelanggaran batas fisika cahaya ($RTT > 120\\text{ ms}$) dan mengeluarkan laporan sanggahan matematis eksak.
  - *Kasus Batas*: Batas toleransi jarak 0 (komputasi satu mesin memori bersama); sistem harus beralih ke batas latensi bus QPI/UPI.
- **Rubrik Penilaian Mandiri**: 40% Verifikasi Batasan Fisika Rigor, 30% Pemodelan RTT Geografis Eksak, 30% Laporan Diagnostik Otomatis Terperinci."""
    },
    3: {
        "trace": """#### Tabel Penelusuran Loop Umpan Balik & Bifurkasi Sistemik (Systems Thinking)
| Langkah / Waktu Diskret (t) | Variabel State / Level Stok | Sinyal Masuk / Laju Aliran | Mekanisme Umpan Balik | Status Penyangga / Delay | Status Keluaran / Efek Sistemik |
|---|---|---|---|---|---|
| Titik T=0 | Kapasitas Jembatan: Normal | Angin samping: $v = 40\\text{ km/jam}$ | Getaran linier vertikal teredam | Redaman struktur $\\zeta = 0.05$ | Osilasi teredam stabil amplitudo kecil |
| Titik T=1 | Mulai Vortex Shedding | $v = 65\\text{ km/jam}$ konstan | Pelepasan pusaran angin berkala | Pusaran membentuk gaya angkat bergantian | Frekuensi dorongan angin mendekati frekuensi alami |
| Titik T=2 | Transisi Torsi Aeroelastik | Pusat massa tergeser | Gerakan jembatan mengubah sudut serang angin | Umpan balik positif non-linier terbentuk | Redaman efektif berubah menjadi negatif ($\\zeta_{eff} < 0$) |
| Titik T=3 | Resonansi Meledak | Energi kinetik terakumulasi | Osilasi puntir melipatgandakan torsi aerodinamis | Deformasi gelagar baja melampaui elastisitas | Amplitudo puntir mencapai $\\pm 45^\\circ$ |
| Titik T=4 | Keruntuhan Total | Batas luluh kabel terlampaui | Sambungan penggantung putus berantai | Kaskade kegagalan mekanik | Gelagar tengah runtuh jatuh ke selat |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Runtuhnya Jembatan Tacoma Narrows Akibat Mengabaikan Kopling Resonansi Aeroelastik Sistemik (1940)",
            "chronology": """- **Kronologi & Konteks Sejarah**: Pada 7 November 1940, jembatan gantung Tacoma Narrows di Washington runtuh akibat hembusan angin konstan berkecepatan 68 km/jam, hanya empat bulan setelah dibuka untuk umum.
- **Akar Masalah Sistemik**: Insinyur mendesain jembatan dengan pendekatan reduksionis statis, mengasumsikan angin hanya memberikan beban dorong horizontal. Mereka mengabaikan umpan balik dinamis kopling aeroelastik (*flutter*): pergerakan jembatan mengubah sudut serang angin, yang menghasilkan gaya angkat berlawanan fasa dan mengubah koefisien redaman sistem menjadi negatif, memompa energi ke mode puntir hingga jembatan terpelintir hancur.""",
            "snippet": """```python
# Simulasi Runge-Kutta Orde 4: Loop Umpan Balik Negatif Menjadi Positif (Aeroelastic Flutter)
import numpy as np

def simulate_aeroelastic_system(t_max=60.0, dt=0.01, wind_speed=18.0):
    # theta: sudut puntir jembatan (radian), omega: kecepatan sudut (rad/s)
    steps = int(t_max / dt)
    time = np.linspace(0, t_max, steps)
    theta = np.zeros(steps)
    omega = np.zeros(steps)
    
    # Kondisi awal gangguan kecil
    theta[0] = 0.01
    omega[0] = 0.0
    
    # Parameter sistem
    I = 1000.0   # Momen inersia
    k = 4000.0   # Kekakuan torsional
    c_base = 20.0 # Redaman struktural pasif
    
    for i in range(steps - 1):
        t = time[i]
        th = theta[i]
        om = omega[i]
        
        # Gaya aerodinamis non-linier: jika angin melebihi batas kritis,
        # dorongan aerodinamis melawan redaman pasif (Redaman Negatif Sistemik)
        aerodynamic_torque = 0.5 * 1.225 * (wind_speed ** 2) * (1.2 * th + 0.15 * (wind_speed / 10.0) * om)
        
        # d_omega/dt = (Torque_aero - k*theta - c_base*omega) / I
        d_omega = (aerodynamic_torque - k * th - c_base * om) / I
        
        # Integrasi Euler-Cromer
        omega[i + 1] = om + d_omega * dt
        theta[i + 1] = th + omega[i + 1] * dt
        
    return time, theta
```""",
            "analysis": """- **Analisis Forensik & Rekayasa Modern**: Tragedi Tacoma Narrows merevolusi disiplin teknik sipil dan arsitektur sistem: tidak ada subsistem yang dapat dianalisis terisolasi jika berinteraksi dengan lingkungan dinamis fluida atau jaringan. Dalam arsitektur perangkat lunak, sistem microservice sering mengalami kegagalan serupa berupa *retry storms*—ketika kegagalan sementara memicu jutaan retry otomatis yang justru mengunci sistem dalam overload permanen."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Bangun simulator Forrester System Dynamics sederhana berbasis model stok dan aliran (*stocks and flows*) untuk memodelkan populasi mangsa-pemangsa Lotka-Volterra.
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan dua stok: `prey_population` ($x$) dan `predator_population` ($y$).
  - Perbarui aliran masuk dan keluar menggunakan integrasi diskret waktu $\\Delta t = 0.01$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Normal*: $x_0 = 100, y_0 = 20, \\alpha=0.1, \\beta=0.002, \\gamma=0.2, \\delta=0.001$.
  - *Keluaran yang Diharapkan*: Terbentuk osilasi fase stabil tertutup periodik; populasi tidak pernah bernilai negatif.
  - *Kasus Batas*: $y_0 = 0$ (tanpa pemangsa); populasi mangsa bertumbuh eksponensial $x(t) = x_0 e^{\\alpha t}$.
- **Rubrik Penilaian Mandiri**: 40% Kestabilan Fase Periodik Lotka-Volterra, 30% Penanganan Nilai Non-Negatif Rigor, 30% Keterbacaan Struktur Aliran & Stok.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan model dinamika sistem antrean microservice yang mereproduksi fenomena *Cascading Failure & Retry Storm* saat salah satu node database mengalami lonjakan penundaan (delay) 200 ms.
- **Petunjuk Perancangan Arsitektur**:
  - Rancang komponen: Klien pemanggil, Gateway API, Worker Pool, dan Database.
  - Klien mengirim request kontinu; jika timeout $> 100\\text{ ms}$, klien melakukan retry instan tanpa jitter eksponensial.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Beban*: 500 req/detik kontinu. Berikan spike latensi 200 ms pada $t=5.0\\text{ detik}$.
  - *Keluaran yang Diharapkan*: Antrean memori worker pool meluap dalam waktu $< 2\\text{ detik}$, menghasilkan kaskade crash di seluruh cluster.
  - *Mitigasi*: Aktifkan Exponential Backoff + Full Jitter dan Circuit Breaker; buktikan sistem berhasil pulih tanpa crash.
- **Rubrik Penilaian Mandiri**: 40% Reproduksi Ulang Retry Storm Deterministik, 30% Implementasi Mitigasi Circuit Breaker Bersih, 30% Analisis Metrik Latensi P99.

### Tingkat 3: Mahir
- **Tugas**: Rancang pustaka simulasi loop umpan balik terdistribusi yang mendeteksi munculnya loop umpan balik positif berbahaya (*runaway reinforcing loops*) dalam grafik metrik telemetri runtime menggunakan analisis nilai eigen matriks Jacobian.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung matriks Jacobian sistem pada setiap jendela waktu $\\Delta T$.
  - Lakukan dekomposisi nilai eigen; jika terdapat nilai eigen dengan bagian riil positif $\\text{Re}(\\lambda_i) > 0$, picu alarm divergensi sistemik instan sebelum saturasi tercapai.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan Uji*: Sistem 4-dimensi coupled ODE yang bertransisi dari spiral stabil ke limit cycle bifurkasi Hopf.
  - *Keluaran yang Diharapkan*: Sistem mendeteksi titik bifurkasi tepat saat $\\text{Re}(\\lambda) = 0$ melintasi sumbu imajiner.
  - *Kasus Batas*: Matriks singular atau rank-deficient; pustaka wajib menerapkan regularisasi Tikhonov sebelum evaluasi eigen.
- **Rubrik Penilaian Mandiri**: 40% Deteksi Bifurkasi Jacobian Riil, 30% Robustness Aljabar Matriks NumPy/SciPy, 30% Dokumentasi Fondasi Teori Kontrol."""
    },
    4: {
        "trace": """#### Tabel Penelusuran Falsifikasi Epistemologis & Audit Anomali Forensik
| Langkah / Tahap Investigasi | Komponen / Entitas Hipotesis | Input / Data Eksperimen | Uji Falsifikasi Popperian | Status Verifikasi / Metrik Forensik | Kesimpulan Ilmiah / Vonis |
|---|---|---|---|---|---|
| Langkah 0: Klaim | Publikasi Makalah | Klaim transistor organik molekul tunggal | Hipotesis: Konduktansi $G$ mengikuti efek medan | Data publikasi diterima jurnal prestisius | Klaim revolusi teknologi silikon diakui |
| Langkah 1: Replikasi | Laboratorium Independen | Upaya replikasi di Princeton & Cornell | Eksperimen ulang dengan parameter identik | Sintesis gagal; perangkat menunjukkan resistansi isolator | Anomali replikasi: Hasil eksperimen tidak dapat diulang |
| Langkah 2: Audit Bitwise | Investigasi Forensik | Perbandingan grafik noise pada suhu 5K vs 250K | Analisis residual noise kurva $I-V$ antar molekul | Pola kurva derau identik hingga level piksel ($r = 1.0$) | Hukum fisika dilanggar: Fluktuasi termal termodinamika lenyap |
| Langkah 3: Konfrontasi | Uji Benford & Residua | Data mentah laboratorium Schön | Pencarian catatan buku laboratorium asli | Komite menemukan seluruh file raw data dihapus dari komputer | Bukti fabrikasi matematis terbukti tak terbantahkan |
| Langkah 4: Falsifikasi | Konsensus Ilmiah | Retraksi 28 makalah di Science & Nature | Hipotesis Schön gugur secara permanen | Gelar doktor ditarik, laboratorium ditutup | Kebenaran empiris ditegakkan via falsifikasi formal |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Skandal Falsifikasi Semikonduktor Bell Labs Jan Hendrik Schön (2002)",
            "chronology": """- **Kronologi & Konteks Sejarah**: Pada tahun 2000–2001, Jan Hendrik Schön, seorang fisikawan muda di Bell Labs, mempublikasikan puluhan makalah terobosan yang mengklaim telah menciptakan transistor skala molekul tunggal dan superkonduktor berbasis karbon (fullerene). Ia memenangkan berbagai penghargaan bergengsi dan dianggap sebagai calon peraih Nobel.
- **Akar Masalah Epistemologis**: Klaim Schön runtuh ketika fisikawan lain menyadari bahwa grafik hasil eksperimen untuk dua perangkat yang sepenuhnya berbeda—bahkan diuji pada suhu yang berbeda (5 Kelvin vs 250 Kelvin)—memiliki pola derau latar belakang (*background noise*) yang identik secara piksel-demi-piksel. Schön tidak melakukan eksperimen riil, melainkan menghasilkan grafik menggunakan persamaan fungsi matematika yang sama lalu menyalin kurvanya.""",
            "snippet": """```python
# Analisis Forensik Derau: Memvalidasi Integritas Data Eksperimen vs Fabrikasi Matematika
import numpy as np

def detect_fabricated_experimental_curves(curve_a: np.ndarray, curve_b: np.ndarray, tolerance: float = 1e-6) -> dict:
    \"\"\"
    Mendeteksi apakah dua kurva eksperimental independen disalin secara artifisial
    dengan membandingkan korelasi residual derau frekuensi tinggi.
    Dua eksperimen fisik riil pada suhu berbeda TIDAK PERNAH memiliki derau termal identik.
    \"\"\"
    assert len(curve_a) == len(curve_b), "Panjang vektor data harus identik"
    
    # Ekstraksi derau dengan menghapus tren sinyal frekuensi rendah (High-pass filter diferensial)
    noise_a = np.diff(curve_a)
    noise_b = np.diff(curve_b)
    
    # Korelasi Pearson antar-derau
    covariance = np.cov(noise_a, noise_b)[0, 1]
    std_a = np.std(noise_a)
    std_b = np.std(noise_b)
    
    correlation = covariance / (std_a * std_b) if (std_a * std_b) > 0 else 0.0
    identical_points = np.sum(np.abs(curve_a - curve_b) < tolerance)
    identical_ratio = identical_points / float(len(curve_a))
    
    is_fabricated = (correlation > 0.95) or (identical_ratio > 0.80)
    
    return {
        "noise_correlation": correlation,
        "identical_ratio": identical_ratio,
        "verdict": "FABRICATED_FRAUD" if is_fabricated else "AUTHENTIC_PHYSICAL_DATA"
    }
```""",
            "analysis": """- **Analisis Epistemologis & Standar Modern**: Skandal Schön adalah demonstrasi nyata prinsip falsifikasi Karl Popper: sains bukanlah akumulasi klaim otoritas, melainkan kesiapan sebuah klaim untuk diuji dan digugurkan secara empiris. Dalam rekayasa perangkat lunak modern, hal ini melandasi pengujian otomatis mutasi (*mutation testing*) dan reproducible builds: jika sistem tidak dapat direplikasi secara deterministik oleh pihak luar, sistem tersebut tidak dapat dipercaya."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Buat fungsi verifikasi kepatuhan Hukum Benford (*Benford's Law*) untuk menguji keaslian sekumpulan data numerik transaksi keuangan atau hasil eksperimen.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung distribusi digit pertama ($d \\in \\{1..9\\}$) dari dataset.
  - Bandingkan dengan distribusi teoritis: $P(d) = \\log_{10}(1 + 1/d)$ menggunakan uji Chi-Square Goodness-of-Fit.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Dataset Asli*: Data transaksi populasi kota atau neraca akuntansi nyata ($p > 0.05$).
  - *Dataset Palsu*: Angka acak seragam $\\mathcal{U}(100, 999)$ di mana digit 1..9 berfrekuensi setara ($p < 0.001$, indikasi manipulasi buatan).
  - *Kasus Batas*: Angka dengan nilai 0 atau negatif; fungsi wajib mengambil nilai mutlak dan mengabaikan nilai 0 sebelum evaluasi digit pertama.
- **Rubrik Penilaian Mandiri**: 40% Formula Benford & Uji Chi-Square Tepat, 30% Filter Angka Negatif/Nol Defensif, 30% Interpretasi Signifikansi Statistik Terbaca.

### Tingkat 2: Menengah
- **Tugas**: Bangun framework audit otomatis *Reproducible Pipeline Validator* yang menjalankan sebuah skrip eksperimen data tiga kali pada environment terisolasi dan membandingkan hash SHA-256 dari seluruh artefak output.
- **Petunjuk Perancangan Arsitektur**:
  - Isolasi eksekusi subprocess dengan seed pseudo-random number generator (`PYTHONHASHSEED`, `np.random.seed`) yang dipatok konstan.
  - Verifikasi bahwa ketiadaan determinisme diidentifikasi sebagai kegagalan reproduktibilitas ilmiah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Uji Deterministik*: Skrip sorting dan matriks deterministik menghasilkan SHA-256 identik pada 3 run berturut-turut.
  - *Uji Non-Deterministik*: Skrip yang membaca `/dev/urandom` atau iterasi set Python yang tidak terurut; framework harus mendeteksi inkonsistensi hash dan menolak pipeline.
  - *Kasus Batas*: File output berukuran 0 byte; sistem wajib melempar exception 'EmptyArtifactError'.
- **Rubrik Penilaian Mandiri**: 40% Mekanisme Audit Hash SHA-256 Bersih, 30% Deteksi Flakiness/Non-determinisme Akurat, 30% Pengelolaan Isolasi Subprocess Aman.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin pembuktian *Property-Based Falsification Engine* (serupa dengan Hypothesis di Python / QuickCheck di Haskell) yang secara aktif mencoba meruntuhkan invarian matematika fungsi pengguna dengan mencari kasus sanggahan terkecil (*minimal counterexample via shrinking*).
- **Petunjuk Perancangan Arsitektur**:
  - Bangun generator nilai uji cerdas yang memprioritaskan nilai batas: float `NaN`, `+Inf`, `-Inf`, `0.0`, `-0.0`, subnormal, dan integer ekstrem ($2^{31}-1, -2^{31}$).
  - Terapkan mekanisme reduksi kasus uji (*shrinking algorithm*) untuk menyusutkan masukan yang memicu kegagalan ke bentuk paling sederhana.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Properti Uji*: Klaim keliru $\\forall a, b \\in \\mathbb{R}: (a + b)^2 > a^2 + b^2$.
  - *Keluaran yang Diharapkan*: Engine menemukan penyangkal $a=0, b=0$ atau nilai berlawanan tanda dalam waktu $< 50\\text{ ms}$ dan menyusutkannya ke representasi minimal.
  - *Kasus Batas*: Fungsi yang membutuhkan waktu eksekusi lama; engine harus memiliki timeout guard per evaluasi invariant.
- **Rubrik Penilaian Mandiri**: 40% Mesin Falsifikasi & Shrinking Efektif, 30% Penetrasi Boundary Value Lengkap, 30% Arsitektur Engine Modular & Bebas Dependensi Eksternal."""
    },
    5: {
        "trace": """#### Tabel Penelusuran Evaluasi Logika Orde Pertama & Resolusi Paradoks Russell
| Langkah / Tahap Deduksi | Struktur Kalimat / Proposisi | Premis / Aksioma Masukan | Operasi Unifikasi & Inferensi | Status Komprehensif Himpunan | Status Evaluasi / Kontradiksi |
|---|---|---|---|---|---|
| Langkah 0: Aksioma Naif | Skema Komprehensif Bebas | $\\exists S, \\forall x: x \\in S \\iff P(x)$ | Pembentukan himpunan dari predikat sembarang | Bebas tanpa pembatasan tipe semesta | Aksioma Frege diterima |
| Langkah 1: Konstruksi | Pembentukan Himpunan Russell | Predikat: $P(x) \\equiv x \\notin x$ | Definisikan himpunan $R = \\{x \\mid x \\notin x\\}$ | Objek $R$ diakui sebagai elemen himpunan legal | Himpunan anomali terbentuk |
| Langkah 2: Evaluasi $R \\in R$ | Substitusi Kasus A | Asumsikan $R \\in R$ bernilai Benar | Berdasarkan definisi: $R \\in R \\implies R \\notin R$ | Kontradiksi langsung: Benar $\\implies$ Salah | Kasus A runtuh |
| Langkah 3: Evaluasi $R \\notin R$ | Substitusi Kasus B | Asumsikan $R \\notin R$ bernilai Benar | Berdasarkan definisi: $R \\notin R \\implies R \\in R$ | Kontradiksi langsung: Salah $\\implies$ Benar | Kasus B runtuh |
| Langkah 4: Resolusi ZFC | Aksioma Pemisahan (*Aussonderung*) | Batasi komprehensif ke subset: $\\{x \\in A \\mid P(x)\\}$ | Russell Paradox mustahil terbentuk karena $R \\notin R$ membuktikan $R$ bukan himpunan | Hirarki tipe ditegakkan | Ledakan logika (*Ex Falso Quodlibet*) dicegah |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Krisis Fondasi Paradoks Russell pada Teori Himpunan Naif Frege (1901)",
            "chronology": """- **Kronologi & Konteks Sejarah**: Pada tahun 1902, matematikawan Jerman Gottlob Frege sedang menyelesaikan jilid kedua adikaryanya, *Grundgesetze der Arithmetik*, yang mendeduksi seluruh hukum matematika dari logika formal murni. Sebelum buku dicetak, Bertrand Russell mengirimkan surat singkat yang mendemonstrasikan paradoks fatal pada Aksioma V Frege.
- **Akar Masalah Logika**: Frege menggunakan skema komprehensif naif: untuk sembarang predikat $P(x)$, ada himpunan $\{x \mid P(x)\}$. Russell mengonstruksi $R = \{x \mid x \notin x\}$. Jika $R \in R$, maka $R \notin R$; jika $R \notin R$, maka $R \in R$. Dalam logika klasik, adanya satu kontradiksi memicu prinsip ledakan (*Principle of Explosion / Ex Falso Quodlibet*), membuat sistem membuktikan klaim apa pun bernilai benar, meruntuhkan seluruh fondasi matematika Frege.""",
            "snippet": """```python
# Evaluator Logika Proposisional & Detektor Kontradiksi Russell
class PropositionalLogicEvaluator:
    def __init__(self):
        pass

    def evaluate_truth_table(self, formula_func, variables: list) -> dict:
        \"\"\"
        Menghasilkan tabel kebenaran lengkap untuk memeriksa Tautologi atau Kontradiksi.
        \"\"\"
        import itertools
        results = []
        is_tautology = True
        is_contradiction = True

        for values in itertools.product([False, True], repeat=len(variables)):
            env = dict(zip(variables, values))
            res = formula_func(env)
            results.append((env, res))
            if res:
                is_contradiction = False
            else:
                is_tautology = False

        return {
            "is_tautology": is_tautology,
            "is_contradiction": is_contradiction,
            "table": results
        }

# Demonstrasi Kontradiksi Russell: (R_in_R <==> not R_in_R) selalu False
def russell_paradox_statement(env):
    # env['R_in_R'] merepresentasikan proposisi R in R
    r = env['R_in_R']
    return (r and not r) or (not r and r)  # r <=> ~r ekuivalen kontradiksi mutlak

evaluator = PropositionalLogicEvaluator()
audit = evaluator.evaluate_truth_table(russell_paradox_statement, ['R_in_R'])
assert audit["is_contradiction"] is True, "Pernyataan Russell wajib terbukti kontradiksi mutlak!"
```""",
            "analysis": """- **Analisis Logika & Dampak Komputasi**: Krisis Russell melahirkan Teori Tipe (*Type Theory*) oleh Russell-Whitehead dan Aksioma Zermelo-Fraenkel (ZFC). Dalam ilmu komputer, Teori Tipe adalah fondasi langsung dari sistem tipe pada kompilator bahasa modern (Rust, Haskell, TypeScript, Scala). Sistem tipe kompilator mencegah self-referential paradox serupa dengan melarang sebuah tipe memuat dirinya sendiri secara tak terikat tanpa pointer tak langsung (*infinite size struct indirection*)."""
        },
        "exercise": """### Tingkat 1: Dasar
- **Tugas**: Implementasikan parser ekspresi logika proposisional dan generator tabel kebenaran lengkap untuk variabel boolean $P, Q, R$.
- **Petunjuk Perancangan Arsitektur**:
  - Dukung operator logika standar: `AND` ($\\land$), `OR` ($\\lor$), `NOT` ($\\neg$), `IMPLIES` ($\\implies$), dan `IFF` ($\\iff$).
  - Evaluasi ekspresi menggunakan pohon sintaks abstrak (AST) atau parsing Shunting-Yard.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Hukum De Morgan*: `NOT (P AND Q)` dievaluasi terhadap `(NOT P) OR (NOT Q)`.
  - *Keluaran yang Diharapkan*: Seluruh $2^2 = 4$ baris tabel kebenaran menghasilkan nilai evaluasi identik (Tautologi Terverifikasi).
  - *Kasus Batas*: Ekspresi dengan tanda kurung bersarang dalam: `((P IMPLIES Q) AND (Q IMPLIES R)) IMPLIES (P IMPLIES R)` (Silogisme Hipotetis); wajib terbukti tautologi 100%.
- **Rubrik Penilaian Mandiri**: 40% Evaluasi Operator Boolean Eksak, 30% Parsing Tanda Kurung Bersarang Bebas Cacat, 30% Format Tampilan Tabel Bersih.

### Tingkat 2: Menengah
- **Tugas**: Bangun pemecah masalah kepuasan proposisional (SAT Solver) sederhana menggunakan algoritma Davis-Putnam-Logemann-Loveland (DPLL) pada formula dalam bentuk Conjunctive Normal Form (CNF).
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan optimasi dasar DPLL: *Unit Propagation* dan *Pure Literal Elimination*.
  - Gunakan penelusuran rekursif dengan *backtracking* saat pencabangan tebakan nilai boolean.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Masukan SAT*: Formula CNF 3-SAT sederhana yang dapat dipenuhi: `[[1, 2], [-1, 3], [-2, -3]]`.
  - *Keluaran yang Diharapkan*: Mengembalikan status `SATISFIABLE` beserta pemetaan variabel (misal `x1=True, x2=False, x3=True`).
  - *Masukan UNSAT*: Formula kontradiksi eksplisit: `[[1], [-1]]`. Solver harus mengembalikan `UNSATISFIABLE` seketika.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Unit Propagation & DPLL Benar, 30% Backtracking Bersih Tanpa Memory Leak, 30% Ketepatan Deteksi SAT vs UNSAT.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin unifikasi resolusi logika orde pertama (*First-Order Logic Resolution Refutation Prover*) yang membuktikan keabsahan argumen silogisme formal.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan algoritma unifikasi Robinson untuk menyelaraskan literal dengan variabel dan konstanta (`unify(P(x), P(Socrates))`).
  - Terapkan eliminasi implikasi, standarisasi variabel, skolemization, dan konversi ke Clause Form sebelum resolusi refutasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Argumen Uji*: Premis 1: $\\forall x (\\text{Man}(x) \\implies \\text{Mortal}(x))$, Premis 2: $\\text{Man}(\\text{Socrates})$. Kesimpulan yang dinegasi: $\\neg \\text{Mortal}(\\text{Socrates})$.
  - *Keluaran yang Diharapkan*: Prover menghasilkan klausa kosong (*empty clause* $\\square$) melalui resolusi unifikasi, membuktikan argumen valid secara deduktif.
  - *Kasus Batas*: Siklus unifikasi tanpa batas (*Occurs Check failure*, misal mencoba menyelaraskan $x$ dengan $f(x)$); algoritma wajib menggagalkan unifikasi.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Unifikasi Robinson Lengkap dengan Occurs Check, 30% Mesin Resolusi Refutasi Terbukti Memutus Klausa Kosong, 30% Kerapian Struktur Data Predikat & Term."""
    }
}
