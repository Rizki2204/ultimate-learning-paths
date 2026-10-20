# scripts/encyclopedia/tier_0_1_addon.py
"""
Rich encyclopedic technical modules for Topics 2, 3, 4, 5, 6, 7, 11, 18, 19, 21.
Each topic includes first-principles intuition, KaTeX mathematics, Mermaid architectures,
executable Python code, industrial pitfalls, 3-level exercises, and direct web resource links.
"""

TOPIC_DATA_0_1_ADDON = {
    2: {
        "intuition": """
Bayangkan Anda ingin membuat kue bolu. Kebanyakan orang menggunakan 'penalaran dengan analogi': mereka melihat koki lain menggunakan tepung terigu merk X dan memanggang 30 menit, lalu menirunya tanpa paham alasannya. Jika tepung merk X habis, mereka panik dan berhenti.

Sebaliknya, **First-Principles Thinking (Penalaran Prinsip Pertama)** membongkar kue tersebut hingga ke level kimia dasar:
- Apa fungsi tepung? Menyediakan protein gluten untuk membentuk jaring penahan gas.
- Apa fungsi telur? Emulsifier (lesitin) dan protein koagulan saat panas.
- Apa fungsi ragi/baking powder? Menghasilkan gas $CO_2$.
- Apa fungsi panas? Denaturasi protein dan gelatinisasi pati.

Ketika Anda memahami hukum dasar termodinamika dan biokimiawi kue, Anda tidak terikat resep siapa pun. Anda bisa mengganti gandum dengan tepung almond + xanthan gum, atau mendesain roket SpaceX dari bahan baku baja mentah alih-alih membeli modul kedirgantaraan seharga jutaan dolar yang dijual kontraktor militer.
[📖 Pelajari: Feynman's First Principles Lecture](https://www.feynmanlectures.caltech.edu/)
""",
        "theory": r"""
### 2.1 Dekonstruksi Aksiomatik & Reduksi Cartesian ([Stanford Encyclopedia: Scientific Reduction](https://plato.stanford.edu/entries/scientific-reduction/))
Penalaran prinsip pertama memformalkan suatu masalah kompleks ke dalam graf dependensi terarah (DAG) aksioma dasar:
Setiap proposisi $P$ diuji keabsahannya dengan membuktikan bahwa $P$ diturunkan dari himpunan aksioma fundamental $\mathcal{A} = \{A_1, A_2, \dots, A_n\}$ melalui aturan inferensi valid $\vdash$:
$$\mathcal{A} \vdash P$$
Jika terdapat proposisi antara $Q$ yang dipercaya hanya karena konsensus sosial atau tradisi tanpa bukti $\mathcal{A} \vdash Q$, maka $Q$ diklasifikasikan sebagai *analogi spekulatif* dan harus dieliminasi.

### 2.2 Dekonstruksi Biaya dan Batas Fisika Landauer ([Landauer Limit Paper: IBM Journal](https://doi.org/10.1147/rd.53.0183))
Batas teoritis mutlak efisiensi suatu proses ditentukan oleh hukum kekekalan massa, energi, dan termodinamika. Batas disipasi energi minimum untuk menghapus 1 bit informasi pada suhu $T$:
$$E_{\min} = k_B T \ln 2$$
Di mana:
- $k_B = 1.380649 \times 10^{-23} \text{ J/K}$ (Konstanta Boltzmann)
- $T$ adalah suhu absolut dalam Kelvin.
Segala inefisiensi di atas $E_{\min}$ adalah murni masalah rekayasa teknik (*engineering artifact*), bukan batasan hukum alam.
""",
        "internals": """
```mermaid
flowchart TD
    Problem["Masalah Kompleks: Biaya Baterai EV $600/kWh"] --> Decomp["Dekonstruksi Material Dasar (BHP)"]
    Decomp --> Mat1["Bahan Baku Kimia: Nikel, Kobalt, Litium, Besi"]
    Decomp --> Mat2["Energi Pemrosesan: Panas Smelting & Pemurnian"]
    Decomp --> Mat3["Separator Membran & Casing Aluminium"]
    Mat1 & Mat2 & Mat3 --> Sum["Jumlah Nilai Komoditas Pasar: $80/kWh"]
    Sum --> Delta["Celah Nilai = $520/kWh Adalah Inefisiensi Rantai Pasok!"]
    Delta --> Rebuild["Rekonstruksi Proses Manufaktur dari Prinsip Pertama (Dry Electrode)"]
```
Proses internal first-principles thinking:
1. **Identifikasi Asumsi Terselubung**: Catat semua klaim yang dianggap 'fakta industri' yang belum pernah diuji secara empiris.
2. **Isolasi Batas Fisik/Matematis**: Turunkan batas atas teoritis (Teorema Carnot, Efisiensi Shannon, Batas Betz).
3. **Rekonstruksi Solusi Optimal**: Bangun kembali alur proses dari nol mutlak menuju batas teoritis tanpa memperdulikan kebiasaan industri yang berlaku saat ini.
""",
        "code_block": '''def first_principles_cost_breakdown(market_price: float, raw_materials: dict[str, tuple[float, float]]) -> dict:
    """
    Menganalisis margin inefisiensi industri menggunakan first-principles deconstruction.
    raw_materials: {nama_elemen: (kuantitas_kg, harga_pasar_per_kg)}
    """
    total_material_cost = sum(qty * price for qty, price in raw_materials.values())
    inefficiency_overhead = market_price - total_material_cost
    reduction_potential_pct = (inefficiency_overhead / market_price) * 100.0
    
    return {
        "market_price": market_price,
        "fundamental_floor": total_material_cost,
        "overhead_waste": inefficiency_overhead,
        "potential_improvement_pct": reduction_potential_pct
    }

# Simulasi dekonstruksi biaya modul baterai LiFePO4 per kWh
battery_elements = {
    "Lithium Carbonate": (0.25, 14.50), # kg, $/kg
    "Iron Phosphate (FePO4)": (1.10, 2.20),
    "Graphite Anode": (0.85, 4.00),
    "Copper Foil": (0.60, 9.00),
    "Aluminum Casing": (0.50, 2.80),
    "Electrolyte & Separator": (0.40, 6.50)
}

result = first_principles_cost_breakdown(market_price=160.0, raw_materials=battery_elements)
print(f"Harga Pasar: ${result['market_price']}/kWh")
print(f"Batas Bawah Material: ${result['fundamental_floor']:.2f}/kWh")
print(f"Potensi Disrupsi Rekayasa: {result['potential_improvement_pct']:.1f}%")
''',
        "pitfalls": """
1. **Analogy Masquerading as First Principles**: Mengutip 'best practice' Google atau Netflix sebagai prinsip pertama padahal itu adalah solusi spesifik konteks organisasi mereka.
2. **Infinite Regress Trap**: Menganalisis masalah bisnis perangkat lunak hingga ke level mekanika kuantum sub-atomik yang tidak relevan dengan tingkat abstraksi masalah.
3. **Mengabaikan Biaya Transisi & Gesekan Riil**: Mengasumsikan bahwa jika batas fisik memungkinkan penghematan 80%, maka implementasi dapat dilakukan instan tanpa memperhitungkan hukum termodinamika sekunder (keausan mekanis, kerugian resistansi internal).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Dekonstruksi Produk Komputasi
Pilihlah salah satu layanan komputasi cloud (misal: AWS S3 $0.023/GB/bulan). Dekonstruksi harga ini ke harga fisik drive enterprise NVMe/HDD mentah, konsumsi listrik watt per drive, biaya pendinginan PUE datacenter, dan redundansi Reed-Solomon $8+4$. Hitung rasio markup biaya cloud.

### Tingkat 2 (Menengah) - Analisis Efisiensi Algoritma dari Prinsip Pertama
Diberikan sebuah algoritma sorting array $N$ elemen. Buktikan secara first principles informasi matematis mengapa perbandingan pairwise tidak akan pernah bisa melampaui batas $O(N \log N)$ (hubungkan dengan pohon keputusan biner dan permutasi $N!$).

### Tingkat 3 (Mahir) - Reduksi Kompleksitas Sistem Terdistribusi
Rancang arsitektur sistem pesan instan berskala 100 juta pengguna harian dari prinsip pertama batas jaringan: kecepatan cahaya di serat optik ($200.000 \\text{ km/s}$), latensi RTT antar benua ($70 \\text{ ms}$), dan batas memori RAM server per socket TCP. Tentukan secara matematis berapa server minimum mutlak yang dibutuhkan.

#### Rubrik Penilaian
- **40% Ketepatan Isolasi Aksioma**: Mampu memisahkan hukum alam/matematika dari sekadar konvensi masa lalu.
- **30% Ketelitian Kuantitatif**: Perhitungan berbasis angka riil dan satuan metrik SI yang konsisten.
- **30% Kelayakan Solusi Rekonstruksi**: Arsitektur baru yang diusulkan tidak melanggar hukum konservasi energi/informasi.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The Feynman Lectures on Physics](https://www.feynmanlectures.caltech.edu/) | Kuliah legendaris Richard Feynman membongkar fisika dari prinsip pertama. |
| 🎓 Kuliah Terbuka | [MIT OCW 18.06SC Linear Algebra & First Principles](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) | Rekonstruksi geometri ruang dan aljabar matriks dari aksioma basis. |
| 🔬 Makalah Seminal | [Irreversibility and Heat Generation in the Computing Process (Landauer, 1961)](https://doi.org/10.1147/rd.53.0183) | Pembuktian batas termodinamika mutlak pada manipulasi informasi. |
| 💻 Lab Interaktif | [Desmos Graphing Scientific Tool](https://www.desmos.com/calculator) | Eksplorasi hubungan kurva fisis dan dekonstruksi fungsi polinomial. |
"""
    },
    3: {
        "intuition": """
Pernahkah Anda mencoba mengatur suhu air di shower air panas hotel lama? Anda memutar keran ke kanan karena air terasa dingin. Tidak ada perubahan selama 5 detik, jadi Anda memutar keran lebih jauh. Tiba-tiba, 3 detik kemudian air menyembur sangat panas seperti mendidih! Anda panik dan memutar keran habis ke kiri. 5 detik kemudian air berubah menjadi es dingin. Anda terjebak dalam osilasi liar.

Ini adalah **Systems Thinking (Berpikir Sistem)**. Masalah di dunia nyata jarang berbentuk sebab-akibat lurus ($A \\to B$). Hampir semua sistem nyata memiliki:
1. **Feedback Loops (Umpan Balik)**: Efek kembali memengaruhi sebab.
2. **Delays (Jeda Waktu)**: Respon sistem tidak instan.
3. **Emergence**: Perilaku keseluruhan sistem tidak bisa ditebak hanya dengan mempelajari bagian per bagian (seperti molekul air cair yang basah, padahal atom hidrogen dan oksigen gas tidak basah).
[📚 Pelajari: MIT System Dynamics Course](https://ocw.mit.edu/courses/15-871-introduction-to-system-dynamics-fall-2013/)
""",
        "theory": r"""
### 3.1 Model Matematika Ruang Keadaan Sistem Dinamik Linier ([MIT 18.03 Differential Equations](https://ocw.mit.edu/courses/18-03-differential-equations-spring-2010/))
Suatu sistem dinamik kontinu dengan vektor keadaan $\mathbf{x}(t) \in \mathbb{R}^n$ dan vektor kontrol $\mathbf{u}(t) \in \mathbb{R}^m$ dimodelkan oleh persamaan diferensial matriks:
$$\dot{\mathbf{x}}(t) = \mathbf{A} \mathbf{x}(t) + \mathbf{B} \mathbf{u}(t)$$
$$\mathbf{y}(t) = \mathbf{C} \mathbf{x}(t) + \mathbf{D} \mathbf{u}(t)$$
Kestabilan sistem dievaluasi dari nilai eigen $\lambda_i$ matriks transisi $\mathbf{A}$:
$$\det(\lambda \mathbf{I} - \mathbf{A}) = 0$$
Sistem stabil asimtotik jika dan hanya jika $\text{Re}(\lambda_i) < 0$ untuk setiap nilai eigen $\lambda_i$.

### 3.2 Loop Penguatan vs Penyeimbang & Efek Jeda Waktu (Delays) ([Donella Meadows Systems Model](https://donellameadows.org/systems-thinking-resources/))
Dalam persamaan diferensial dengan jeda waktu $\tau$ (delay differential equation):
$$\frac{dx(t)}{dt} = -k \cdot x(t - \tau)$$
Jika produk penguatan $k \tau > \frac{\pi}{2}$, sistem penyeimbang sederhana (balancing feedback) akan kehilangan stabilitas dan berubah menjadi osilator liar tak teredam (limit cycle).
""",
        "internals": """
```mermaid
graph LR
    subgraph FeedbackArchitecture["Arsitektur Sistem Umpan Balik Tertutup"]
        SetPoint["Nilai Target r(t)"] --> ErrorSum["Error: e(t) = r(t) - y(t)"]
        ErrorSum --> Controller["Kontroler K(s)"]
        Controller --> DelayBlock["Jeda Waktu Transportasi: exp(-s * tau)"]
        DelayBlock --> Plant["Sistem Fisik / Layanan Backend G(s)"]
        Plant --> Output["Output Terukur y(t)"]
        Output --> FeedbackPath["Sensor / Telemetri H(s)"]
        FeedbackPath --> ErrorSum
    end
```
Anatomi kegagalan dalam rekayasa perangkat lunak:
- **Thundering Herd**: Ketika cache kadaluarsa serentak, jutaan request langsung menghantam database. Respon DB melambat (menambah delay $\tau$).
- **Cascading Failure**: Retry otomatis tanpa exponential backoff memperbesar gain loop $k$, mendorong $k\tau > \frac{\pi}{2}$ dan meruntuhkan kluster server seketika.
""",
        "code_block": '''import numpy as np

def simulate_system_dynamics_delay(steps=100, delay_ticks=5, gain=0.35):
    """
    Simulasi numerik efek keterlambatan (delay) pada umpan balik penyeimbang.
    dx/dt = -gain * x(t - delay)
    """
    history = [10.0] * (delay_ticks + 1)
    results = [10.0]
    
    for _ in range(steps):
        delayed_x = history[-delay_ticks - 1]
        # Penyesuaian koreksi berdasarkan informasi masa lalu yang tertunda
        dx = -gain * delayed_x
        current_x = history[-1] + dx
        history.append(current_x)
        results.append(current_x)
        
    return results

trajectory = simulate_system_dynamics_delay(steps=15, delay_ticks=4, gain=0.55)
for step, val in enumerate(trajectory[:10]):
    print(f"Tick {step:02d}: x(t) = {val:+.4f} {'(Osilasi Membesar!)' if abs(val) > 10.0 else ''}")
''',
        "pitfalls": """
1. **Linear Thinking in Nonlinear Worlds**: Mengasumsikan bahwa meningkatkan kapasitas server 2x lipat akan menangani 2x traffic, padahal lock contention database berskala nonlinier kuadratik $O(N^2)$.
2. **Treating Symptoms Instead of Root Feedback Loops**: Mengaktifkan auto-restart saat memori bocor (OOM) alih-alih memperbaiki memory leak, yang pada akhirnya memicu cascading restart di seluruh fleet.
3. **Optimizing Local Subsystems at the Expense of Global Coherence**: Mengoptimalkan throughput komponen A sehingga membanjiri buffer komponen B yang tidak mampu mengonsumsi data, menyebabkan buffer bloat.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Diagram Loop Kausal Sederhana
Gambarkan Causal Loop Diagram (CLD) interaksi antara bug perangkat lunak, kelelahan developer, tekanan deadline manajemen, dan utang teknis (technical debt). Identifikasi mana yang merupakan reinforcing loop ($R$) dan balancing loop ($B$).

### Tingkat 2 (Menengah) - Simulasi Bullwhip Effect Rantai Pasok
Implementasikan skrip simulasi sistem dinamik model Beer Distribution Game (Retailer, Wholesaler, Distributor, Factory) dengan jeda pemesanan 2 siklus. Tunjukkan bagaimana fluktuasi permintaan konsumen sebesar 10% teramplifikasi menjadi 200% di tingkat pabrik.

### Tingkat 3 (Mahir) - Stabilitas Kontrol Autoscaler Kubernetes
Bangun model matematis untuk autoscaler Pod Kubernetes berbasis CPU utilization. Buktikan secara matematis batas waktu cooldown ($t_{\\text{cooldown}}$) minimum agar tidak terjadi *flapping* (pod scale up dan scale down berosilasi terus-menerus tanpa henti).

#### Rubrik Penilaian
- **40% Ketepatan Pemodelan State Space**: Variabel akumulator (stocks) dan aliran (flows) didefinisikan secara tegas.
- **30% Analisis Stabilitas Dinamik**: Mampu menghitung margin kestabilan gain dan delay.
- **30% Penanganan Emergence**: Menyediakan mekanisme mitigasi terhadap failure mode non-lokal.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Thinking in Systems: A Primer (Donella Meadows)](https://donellameadows.org/systems-thinking-resources/) | Kitab suci pemikiran sistem klasik dan dinamika loop umpan balik. |
| 🎓 Kuliah Terbuka | [MIT OCW 15.871 Introduction to System Dynamics](https://ocw.mit.edu/courses/15-871-introduction-to-system-dynamics-fall-2013/) | Metodologi formal pemodelan simulasi sistem kompleks di MIT Sloan. |
| 🔬 Makalah Seminal | [Industrial Dynamics (Jay W. Forrester, 1958)](https://doi.org/10.1287/mnsc.4.4.347) | Paper perintis yang melahirkan sains pemodelan sistem terkomputerisasi. |
| 💻 Lab Interaktif | [Insight Maker System Dynamics Sandbox](https://insightmaker.com/) | Platform visual simulasi stok, aliran, dan loop kausal berbasis browser. |
"""
    },
    4: {
        "intuition": """
Bayangkan Anda tinggal di sebuah desa di mana semua angsa yang pernah dilihat warga berbulu putih. Warga desa membuat 'hukum alam': *Semua angsa di dunia berwarna putih*. Mereka telah mengamati 1.000 angsa putih berturut-turut. Setiap angsa putih baru yang ditemukan tampaknya 'membuktikan' teori mereka.

Namun pada tahun 1697, penjelajah berlayar ke Australia dan melihat seekor **Angsa Hitam (*Cygnus atratus*)**. Hanya dengan **satu pengamatan tunggal**, teori yang didukung 1.000 bukti hancur seketika!

Inilah inti **Filsafat Sains & Falsifikasi Karl Popper**:
1. Anda tidak akan pernah bisa membuktikan suatu teori ilmiah 100% benar secara absolut melalui induksi (karena Anda tidak bisa memeriksa seluruh alam semesta hingga akhir zaman).
2. Sebuah klaim hanya disebut **ilmiah** jika klaim tersebut memiliki syarat pembuktian salah (**falsifiable**).
3. Jika sebuah klaim tidak bisa diuji salah dalam skenario apa pun (misal: 'besok Anda mungkin beruntung atau tidak beruntung'), itu bukan sains, melainkan pseudosains atau dogma.
[📖 Pelajari: Karl Popper - The Logic of Scientific Discovery](https://plato.stanford.edu/entries/popper/)
""",
        "theory": r"""
### 4.1 Masalah Induksi David Hume ([Stanford: Problem of Induction](https://plato.stanford.edu/entries/induction-problem/))
Generalisasi induktif mengasumsikan keteraturan alam (Uniformity of Nature). Dari premis partikular:
$$\forall i \in \{1, \dots, N\}, \quad P(a_i) \text{ bernilai TRUE}$$
Induksi menarik kesimpulan universal:
$$\forall x, \quad P(x)$$
David Hume membuktikan bahwa penalaran ini sirkular: kita mempercayai induksi hanya karena di masa lalu induksi berhasil, yang merupakan penalaran induktif itu sendiri.

### 4.2 Kriteria Demarkasi & Asimetri Falsifikasi Popper ([Popper's Epistemology](https://plato.stanford.edu/entries/popper/))
Terdapat asimetri logis murni antara verifikasi dan falsifikasi dalam kalkulus predikat orde pertama:
- Sejuta pengamatan positif tidak dapat memvalidasi proposisi universal:
$$\neg \left[ \left( \bigwedge_{i=1}^N P(a_i) \right) \implies \forall x P(x) \right]$$
- Namun satu pengamatan kontra-contoh cukup untuk memfalsifikasi secara deduktif melalui *Modus Tollens*:
$$\frac{\forall x (T(x) \implies O(x)), \quad \exists k (T(k) \land \neg O(k))}{\therefore \neg \forall x (T(x) \implies O(x))}$$

### 4.3 Epistemologi Bayesian: Derajat Keyakinan Rasional ([MIT 18.650 Bayesian Inference](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/))
Alih-alih biner benar/salah, paradigma Bayesian memperbarui probabilitas hipotesis $H$ berdasarkan bukti baru $E$:
$$P(H \mid E) = \frac{P(E \mid H) P(H)}{P(E)}$$
Di mana $P(H)$ adalah keyakinan awal (*prior*), $P(E \mid H)$ adalah *likelihood*, dan $P(H \mid E)$ adalah keyakinan yang diperbarui (*posterior*).
""",
        "internals": """
```mermaid
flowchart TD
    Hypothesis["Hipotesis Ilmiah H: Sistem Mampu 100K RPS Latensi < 10ms"] --> Deduce["Deduksi Prediksi Empiris Terukur O"]
    Deduce --> Experiment["Eksperimen Stress Test Terkontrol"]
    Experiment --> Check{"Apakah Terjadi O: Latensi >= 10ms?"}
    Check -- "Ya, Terjadi Deviasi (Modus Tollens)" --> Falsified["Hipotesis Terfalsifikasi: Modifikasi Model Internal!"]
    Check -- "Tidak, Latensi Aman" --> Corroborated["Hipotesis Terkoroborasi Sementara: Uji pada Skala Lebih Ekstrem"]
    Corroborated --> Experiment
```
Siklus Metode Ilmiah Popperian:
1. Formulasi hipotesis yang berani (*bold hypothesis*) dengan ruang pengujian falsifikasi yang luas.
2. Desain eksperimen kejam (*severe test*) yang dirancang khusus untuk menjatuhkan hipotesis.
3. Teori yang lolos uji tidak disebut 'terbukti benar selamanya', melainkan **terkoroborasi** (*corroborated*) sampai eksperimen baru yang lebih presisi menggugurkannya.
""",
        "code_block": '''def bayesian_hypothesis_updater(prior: float, likelihood_if_true: float, likelihood_if_false: float) -> float:
    """
    Menghitung probabilitas posterior hipotesis berdasarkan bukti empiris baru.
    P(H|E) = (P(E|H) * P(H)) / [P(E|H)*P(H) + P(E|~H)*P(~H)]
    """
    marginal_evidence = (likelihood_if_true * prior) + (likelihood_if_false * (1.0 - prior))
    posterior = (likelihood_if_true * prior) / marginal_evidence
    return posterior

# Kasus: Hipotesis H = "Algoritma kompresi baru bebas bug memory corruption"
prior_belief = 0.50 # Skeptis awal 50-50

# Dijalankan pengujian fuzzing 10 juta input acak tanpa crash:
# P(NoCrash | BebasBug) = 1.0
# P(NoCrash | AdaBug) = 0.05 (sangat kecil kemungkinan bug lolos dari 10jt fuzzing)
updated_belief = bayesian_hypothesis_updater(prior=prior_belief, 
                                             likelihood_if_true=1.0, 
                                             likelihood_if_false=0.05)

print(f"Keyakinan Awal (Prior): {prior_belief * 100:.1f}%")
print(f"Keyakinan Pasca Fuzzing Berat (Posterior): {updated_belief * 100:.2f}%")
''',
        "pitfalls": """
1. **Confirmation Bias**: Pengembang perangkat lunak hanya menulis unit test untuk *happy path* (masukan yang mereka tahu akan berhasil), alih-alih merancang test yang sengaja berusaha merusak sistem.
2. **Post-Hoc Rationalization**: Mengubah metrik keberhasilan atau menambah variabel ad-hoc setelah eksperimen gagal agar terlihat seolah-olah hipotesis semula berhasil.
3. **Pseudoscience of Non-reproducibility**: Mempublikasikan performa benchmark ML/Database tanpa merilis seed acak, konfigurasi hardware, dataset lengkap, dan skrip lingkungan.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Audit Falsifiabilitas Pernyataan Teknis
Evaluasi 5 pernyataan arsitektur berikut: tentukan mana yang *falsifiable* dan mana yang tidak:
1. "Arsitektur microservices selalu lebih baik daripada monolit."
2. "Service X memiliki p99 latency di bawah 50ms untuk payload JSON berukuran < 10KB pada throughput 5.000 RPS."
3. "Kecerdasan Buatan Umum (AGI) akan muncul ketika sistem mencapai kesadaran kosmik."
4. "Database NoSQL ini memberikan konsistensi linearizable sesuai spesifikasi Jepsen testing."

### Tingkat 2 (Menengah) - Desain Severe Test untuk Cache Invalidation
Rancang skenario uji empiris berbasis *falsifikasi* untuk membuktikan kelemahan protokol cache invalidation terdistribusi berbasis TTL. Buat skrip stress testing jaringan yang mensimulasikan packet drop dan clock drift antar node.

### Tingkat 3 (Mahir) - Replikasi Krisis Sains dalam Benchmark AI
Ambil sebuah paper ML yang mengklaim metode barunya mengalahkan State-of-the-Art (SOTA). Lakukan pengujian saintifik independen dengan mengubah seed acak sebanyak 50 kali dan menguji pada data di luar domain (out-of-distribution). Analisis signifikansi statistik hasilnya menggunakan uji hipotesis Welch's t-test.

#### Rubrik Penilaian
- **40% Kriteria Falsifiabilitas**: Hipotesis dirumuskan dengan batasan kuantitatif yang jelas dan dapat digugurkan.
- **30% Kontrol Variabel Perancu (Confounding Variables)**: Mengisolasi variabel eksperimen dari noise lingkungan.
- **30% Integritas Replikasi**: Kode eksperimen bersifat deterministik, terbuka, dan dapat direproduksi oleh pihak ketiga.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The Logic of Scientific Discovery (Karl Popper)](https://plato.stanford.edu/entries/popper/) | Karya seminal filsafat sains abad ke-20 mengenai falsifikasi dan metode deduktif. |
| 🎓 Kuliah Terbuka | [MIT OCW 24.111 Philosophy of Science](https://ocw.mit.edu/courses/24-111-philosophy-of-science-spring-2016/) | Kuliah komprehensif epistemologi ilmiah, reduksi, dan struktur revolusi sains. |
| 🔬 Makalah Seminal | [Against Method (Paul Feyerabend, 1975)](https://www.marxists.org/reference/subject/philosophy/works/ge/feyerabe.htm) | Kritik radikal terhadap dogmatisme metode ilmiah monolitik. |
| 💻 Lab Interaktif | [Jepsen Distributed Systems Safety Analysis](https://jepsen.io/analyses) | Contoh nyata falsifikasi ilmiah praktis terhadap klaim konsistensi database modern. |
"""
    },
    5: {
        "intuition": """
Bayangkan seorang hakim di ruang sidang. Seorang jaksa berkata: "Terdakwa pasti pencuri, karena dia terlihat gugup dan kebanyakan pencuri itu gugup!" Hakim yang paham logika akan langsung menolak argumen tersebut karena itu adalah kesalahan berpikir *affirming the consequent*. Gugup bisa disebabkan oleh demam panggung, takut dituduh salah, atau kedinginan.

Dalam dunia komputer dan matematika, kita tidak boleh 'mengira-ngira'. Logika formal adalah **alat pemeriksa kebenaran mekanis**:
- Jika premisnya benar dan aturan penurunannya valid, maka kesimpulannya **dijamin 100% mutlak benar** di alam semesta mana pun!
- Semua compiler bahasa pemrograman, verifier keamanan kriptografi, hingga chip prosesor di dalam smartphone Anda dibangun di atas aturan logika formal ini.
[📚 Pelajari: MIT Logic Course](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/)
""",
        "theory": r"""
### 5.1 Logika Proposisional & Tabel Kebenaran ([Stanford CS103 Mathematical Foundations](https://web.stanford.edu/class/cs103/))
Bahasa formal proposisional didefinisikan secara rekursif atas himpunan variabel proposisional $P, Q, R$ dan perangkai logis:
- Negasi: $\neg P$
- Konjungsi: $P \land Q$
- Disjungsi: $P \lor Q$
- Implikasi Material: $P \implies Q \equiv \neg P \lor Q$
- Bi-implikasi: $P \iff Q \equiv (P \implies Q) \land (Q \implies P)$

### 5.2 Logika Predikat Orde Pertama (First-Order Logic / FOL) ([Open Logic Project](https://openlogicproject.net/))
Menambahkan domain diskursus, fungsi, relasi, dan kuantor:
- Kuantor Universal: $\forall x \, P(x)$ ("untuk setiap $x$, $P(x)$ berlaku")
- Kuantor Eksistensial: $\exists x \, P(x)$ ("terdapat setidaknya satu $x$ sehingga $P(x)$ berlaku")
Hukum De Morgan untuk kuantor:
$$\neg (\forall x \, P(x)) \iff \exists x \, (\neg P(x))$$
$$\neg (\exists x \, P(x)) \iff \forall x \, (\neg P(x))$$

### 5.3 Metode Pembuktian Matematis ([Book of Proof by Richard Hammack](https://www.people.vcu.edu/~rhammack/BookOfProof/))
1. **Bukti Langsung (Direct Proof)**: Asumsikan $P$, buktikan $Q$.
2. **Kontraposisi (Contrapositive)**: Membuktikan $P \implies Q$ melalui ekuivalensi logis $\neg Q \implies \neg P$.
3. **Kontradiksi (Reductio ad Absurdum)**: Asumsikan $P \land \neg Q$, turunkan kontradiksi mutlak $R \land \neg R \equiv \bot$.
4. **Induksi Matematika**:
   - Basis: Buktikan $P(0)$ benar.
   - Langkah Induktif: Buktikan $\forall k, (P(k) \implies P(k+1))$.
   - Kesimpulan: $\forall n \in \mathbb{N}, P(n)$ benar.
""",
        "internals": """
```mermaid
flowchart TD
    Premises["Himpunan Premis Terverifikasi: Gamma"] --> Rule1["Aturan Inferensi: Modus Ponens (A, A -> B |= B)"]
    Rule1 --> Intermediate["Proposisi Antara Terbukti"]
    Intermediate --> Rule2["Aturan Inferensi: Universal Instantiation"]
    Rule2 --> Theorem["Teorema / Kesimpulan Akhir Q (Q.E.D.)"]
```
Mekanisme pembuktian formal (Proof Assistant / SAT Solver):
- **SAT Solvers (DPLL / CDCL)**: Memeriksa apakah suatu formula proposisional dalam bentuk CNF (Conjunctive Normal Form) dapat dipuaskan (*satisfiable*).
- **Curry-Howard Isomorphism**: Korespodensi mendalam antara logika dan ilmu komputer: Proposisi $\equiv$ Tipe Data, Bukti Matematis $\equiv$ Program Komputer yang dapat dieksekusi.
""",
        "code_block": '''def verify_modus_ponens(p: bool, p_implies_q: bool) -> bool:
    """
    Verifikasi mekanis aturan inferensi Modus Ponens:
    Premis 1: P
    Premis 2: P -> Q
    Konklusi: Q
    """
    # Mengingat (P -> Q) ekuivalen dengan (not P or Q)
    # Jika P True dan (P -> Q) True, maka Q harus True.
    assert p is True, "Premis P harus valid"
    assert p_implies_q is True, "Premis implikasi P -> Q harus valid"
    
    # Menemukan nilai kebenaran Q secara deduktif
    q = p and p_implies_q
    return q

# Verifikasi deduksi kebenaran
is_raining = True
rain_implies_wet_ground = True # Jika hujan, maka tanah basah

ground_is_wet = verify_modus_ponens(is_raining, rain_implies_wet_ground)
print(f"Status Kebenaran Deduktif Konklusi: Tanah Basah = {ground_is_wet}")
''',
        "pitfalls": """
1. **Fallacy of Affirming the Consequent**: Menarik kesimpulan $P$ dari premis $(P \implies Q)$ dan $Q$. Contoh: "Jika hujan jalanan basah. Jalanan basah, jadi pasti hujan" (padahal bisa disiram mobil tangki).
2. **Fallacy of Denying the Antecedent**: Menarik kesimpulan $\neg Q$ dari premis $(P \implies Q)$ dan $\neg P$.
3. **Flawed Induction Base Case**: Melakukan pembuktian induktif dengan langkah implikasi $P(k) \implies P(k+1)$ yang benar tetapi dasar induksi $P(0)$ tidak valid, menghasilkan teorem palsu (misal paradoks "semua kuda memiliki warna sama").
""",
        "exercises": """
### Tingkat 1 (Pemula) - Konstruksi Tabel Kebenaran Formal
Buktikan menggunakan tabel kebenaran lengkap ($2^3 = 8$ baris) bahwa hukum distributif logika proposisional berlaku:
$$P \lor (Q \land R) \equiv (P \lor Q) \land (P \lor R)$$

### Tingkat 2 (Menengah) - Pembuktian Ketakhinggaan Bilangan Prima
Tuliskan pembuktian kontradiksi formal Euclid untuk membuktikan bahwa himpunan bilangan prima adalah tak hingga:
1. Asumsikan bilangan prima berhingga: $S = \{p_1, p_2, \dots, p_n\}$.
2. Konstruksi bilangan bulat $N = (p_1 \times p_2 \times \dots \times p_n) + 1$.
3. Buktikan secara deduktif bahwa $N$ memunculkan kontradiksi logis terhadap asumsi awal.

### Tingkat 3 (Mahir) - Pemecah Masalah Kepuasan Boolean (Mini-SAT Solver)
Implementasikan algoritma DPLL (Davis-Putnam-Logemann-Loveland) sederhana dalam Python yang menerima ekspresi logika dalam bentuk CNF dan mengembalikan penugasan variabel Boolean yang memuaskan atau menyatakan formula tidak dapat dipuaskan (UNSAT).

#### Rubrik Penilaian
- **40% Ketelitian Aksiomatik**: Tidak ada lompatan logika implisit atau pembuktian sirkular.
- **30% Ketepatan Penggunaan Kuantor**: Membedakan cakupan kuantor $\forall x \exists y$ dengan $\exists y \forall x$.
- **30% Validitas Algoritmik**: Implementasi DPLL mampu menangani unit propagation dan pure literal elimination secara benar.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Book of Proof (Richard Hammack)](https://www.people.vcu.edu/~rhammack/BookOfProof/) | Panduan standar terbuka untuk metode pembuktian matematika formal. |
| 🎓 Kuliah Terbuka | [MIT OCW 24.241 Logic I](https://ocw.mit.edu/courses/24-241-logic-i-fall-2009/) | Kuliah logika formal proposisional, predikat, dan teori metateori logika. |
| 🔬 Makalah Seminal | [A Machine Program for Theorem-Proving (Davis, Logemann, Loveland, 1962)](https://doi.org/10.1145/368273.368557) | Makalah asli yang mendefinisikan algoritma CDCL/DPLL untuk SAT solving. |
| 💻 Lab Interaktif | [Logic Friday - Boolean Logic Analysis Tool](http://sontrak.com/) | Program visualisasi fungsi boolean, minimalisasi tabel kebenaran, dan gerbang. |
"""
    },
    6: {
        "intuition": """
Bayangkan Anda memiliki kotak mainan. Anda ingin mengelompokkan mainan tersebut:
- Kelompok A: Mainan berwarna merah.
- Kelompok B: Mainan yang memiliki roda.

Apakah ada mainan yang masuk ke kedua kelompok? Ya, mobil balap merah! Itu disebut **Irisan (Intersection)**.
Apakah ada mainan yang masuk kelompok A atau B? Itu disebut **Gabungan (Union)**.

**Teori Himpunan (Set Theory)** adalah fondasi paling dasar dari seluruh matematika modern. Angka 0, 1, 2, garis lurus, matriks, fungsi komputer, dan database relasional SQL yang menyimpan saldo bank Anda, semuanya didefinisikan dari kumpulan objek tak berulang ini.
[📖 Pelajari: Stanford CS103 Mathematical Foundations](https://web.stanford.edu/class/cs103/)
""",
        "theory": r"""
### 6.1 Aksioma Zermelo-Fraenkel (ZFC) & Paradoks Russell ([Stanford: Set Theory](https://plato.stanford.edu/entries/set-theory/))
Paradoks Bertrand Russell menggugurkan teori himpunan naif: Jika $R = \{x \mid x \notin x\}$, apakah $R \in R$?
- Jika $R \in R$, maka menurut definisi $R \notin R$ (kontradiksi).
- Jika $R \notin R$, maka menurut definisi $R \in R$ (kontradiksi).
Solusi: Aksioma ZFC membatasi pembentukan himpunan melalui *Axiom of Specification* dan *Axiom of Foundation*.

### 6.2 Relasi & Sifat-Sifatnya ([Wolfram MathWorld: Equivalence Relation](https://mathworld.wolfram.com/EquivalenceRelation.html))
Relasi biner $R$ pada himpunan $A$ ($R \subseteq A \times A$) disebut **Relasi Ekuivalensi** ($\sim$) jika memenuhi tiga sifat:
1. **Refleksif**: $\forall x \in A, \, x \sim x$
2. **Simetris**: $\forall x, y \in A, \, x \sim y \implies y \sim x$
3. **Transitif**: $\forall x, y, z \in A, \, (x \sim y \land y \sim z) \implies x \sim z$
Relasi ekuivalensi mempartisi himpunan $A$ menjadi kelas-kelas ekuivalensi yang saling lepas (*disjoint partition*).

### 6.3 Karakteristik Fungsi: Injektif, Surjektif, Bijektif ([MIT 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/))
Untuk fungsi $f: A \to B$:
- **Injektif (Satu-ke-Satu)**: $\forall x_1, x_2 \in A, \, f(x_1) = f(x_2) \implies x_1 = x_2$
- **Surjektif (Pada / Onto)**: $\forall y \in B, \, \exists x \in A, \, f(x) = y$
- **Bijektif**: Memenuhi injektif dan surjektif sekaligus, menjamin adanya fungsi invers $f^{-1}: B \to A$.
""",
        "internals": """
```mermaid
graph LR
    Domain["Domain A: {1, 2, 3}"] -- "Fungsi Bijektif f(x) = 2x" --> Codomain["Kodomain / Range B: {2, 4, 6}"]
    Codomain -- "Invers Presisi f^(-1)(y) = y / 2" --> Domain
```
Struktur data himpunan di sistem komputer:
- **Hash Set**: Menggunakan hash table $O(1)$ amortized untuk lookup membership.
- **Bitset / Bit Array**: Operasi union ($\cup$) menggunakan bitwise OR (`|`), intersection ($\cap$) menggunakan bitwise AND (`&`), dieksekusi dalam 1 siklus clock CPU berkecepatan tinggi via instruksi SIMD.
""",
        "code_block": '''def set_theory_operations(set_a: set, set_b: set) -> dict:
    """
    Demonstrasi operasi teori himpunan fundamental.
    """
    return {
        "union (A | B)": set_a.union(set_b),
        "intersection (A & B)": set_a.intersection(set_b),
        "difference (A - B)": set_a.difference(set_b),
        "symmetric_diff (A ^ B)": set_a.symmetric_difference(set_b),
        "is_subset (A <= B)": set_a.issubset(set_b)
    }

a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}
ops = set_theory_operations(a, b)

print(f"Himpunan A: {a}")
print(f"Himpunan B: {b}")
print(f"Irisan (Intersection): {ops['intersection (A & B)']}")
print(f"Beda Simetris: {ops['symmetric_diff (A ^ B)']}")
''',
        "pitfalls": """
1. **Confusing Subset with Element**: Mengira $A \subseteq B$ sama dengan $A \in B$. Himpunan $\{1\}$ adalah subset dari $\{1, 2\}$, tetapi $\{1\}$ bukan elemen dari $\{1, 2\}$.
2. **Assuming Hash Sets are Truly O(1)**: Mengabaikan hash collision attack di mana penyerang sengaja mengirim jutaan kunci dengan nilai hash sama, mereduksi kompleksitas himpunan dari $O(1)$ menjadi $O(N)$ dan melumpuhkan server web.
3. **Float Keys in Hash Sets**: Memasukkan bilangan pecahan floating point (`float`) ke dalam set/dict yang menghasilkan bug kritis karena pembulatan presisi IEEE 754 ($0.1 + 0.2 \neq 0.3$).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Verifikasi Hukum De Morgan Himpunan
Tuliskan skrip Python yang memverifikasi bahwa untuk sembarang himpunan semesta $U$ dan dua subset $A, B \subseteq U$:
$$(A \cup B)^c = A^c \cap B^c \quad \text{dan} \quad (A \cap B)^c = A^c \cup B^c$$

### Tingkat 2 (Menengah) - Partisi Kelas Ekuivalensi Modular
Diberikan relasi ekuivalensi kongruensi modulo $m$ pada himpunan bilangan bulat $\mathbb{Z}$: $a \sim b \iff a \equiv b \pmod m$. Buktikan secara formal bahwa relasi ini refleksif, simetris, dan transitif, lalu bangun fungsi yang mengembalikan himpunan kelas partisi $\mathbb{Z}/m\mathbb{Z}$.

### Tingkat 3 (Mahir) - Implementasi Disjoint-Set Union (Union-Find)
Implementasikan struktur data Union-Find (*Disjoint-Set Forest*) dari nol dengan optimasi *Path Compression* dan *Union by Rank*. Buktikan bahwa kompleksitas waktu amortized operasi adalah $O(\alpha(N))$ di mana $\alpha$ adalah fungsi Inverse Ackermann.

#### Rubrik Penilaian
- **40% Kebenaran Aksiomatik**: Memahami batas formal ZFC dan pembuktian relasi ekuivalensi.
- **30% Efisiensi Algoritmik**: Struktur data himpunan diimplementasikan secara efisien tanpa kebocoran memori.
- **30% Penanganan Edge Cases**: Menangani himpunan kosong $\emptyset$ dan himpunan tak hingga secara tepat.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Elements of Set Theory (Herbert B. Enderton)](https://www.sciencedirect.com/book/9780122384400/elements-of-set-theory) | Buku teks standar universal pengantar teori himpunan aksiomatik ZFC. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.042J Mathematics for Computer Science](https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/) | Matematika diskrit, relasi, fungsi, dan teori himpunan untuk ilmu komputer. |
| 🔬 Makalah Seminal | [Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen (Cantor, 1874)](https://doi.org/10.1515/crll.1874.77.258) | Paper pendiri Georg Cantor yang membuktikan ketaktercacahan bilangan riil. |
| 💻 Lab Interaktif | [Desmos Venn Diagram Sandbox](https://www.desmos.com/calculator) | Eksplorasi interaktif operasi himpunan, diagram Venn, dan aljabar Boolean. |
"""
    },
    7: {
        "intuition": """
Pernahkah Anda bertanya mengapa angka 'sepuluh' ditulis dengan dua digit `10`? Itu hanya karena manusia kebetulan berevolusi dengan sepuluh jari di tangan kita! Jika kita memiliki delapan jari seperti tokoh kartun, kita akan menggunakan basis 8 (Oktal), di mana angka setelah 7 adalah 10.

Komputer tidak memiliki jari biologis. Komputer hanya memiliki jutaan sakelar transistor kecil: nyala (tegangan tinggi $\\approx 3.3\\text{V} = 1$) atau mati (tegangan nol $\\approx 0\\text{V} = 0$). Karena hanya ada dua keadaan, komputer menghitung dalam **Sistem Biner (Basis 2)**.
Memahami sistem bilangan adalah jembatan pertama antara logika abstrak matematika dengan kabel tembaga dan transistor silikon di dalam CPU Anda.
[📚 Pelajari: MIT Computation Structures](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/)
""",
        "theory": r"""
### 7.1 Sistem Nilai Posisi Basis $b$ Polinomial ([Nand2Tetris Course](https://www.nand2tetris.org/))
Setiap bilangan bulat positif $N$ dapat dinyatakan secara unik dalam basis radiks $b \ge 2$:
$$N = \sum_{k=0}^{m-1} d_k \cdot b^k = d_{m-1} b^{m-1} + \dots + d_1 b^1 + d_0 b^0, \quad d_k \in \{0, 1, \dots, b-1\}$$
Konversi antar basis:
- **Biner ke Heksadesimal**: Kelompokkan setiap 4 bit biner menjadi 1 digit heksadesimal ($2^4 = 16$).
  Contoh: $1101_2 = 13_{10} = \text{D}_{16}$.
- **Desimal ke Basis $b$**: Pembagian berulang dengan $b$ menggunakan sisa bagi (*modulo*):
  $$d_k = N \bmod b, \quad N \leftarrow \lfloor N / b \rfloor$$

### 7.2 Aritmatika Biner & Operasi Bitwise ([IEEE Computer Society](https://www.computer.org/))
Operasi penambahan 1-bit Half-Adder:
- Jumlah (*Sum*): $S = A \oplus B$ (Gerbang XOR)
- Bawaan (*Carry*): $C = A \land B$ (Gerbang AND)
Full-Adder 1-bit dengan carry-in $C_{in}$:
$$S = A \oplus B \oplus C_{in}$$
$$C_{out} = (A \land B) \lor (C_{in} \land (A \oplus B))$$
""",
        "internals": """
```mermaid
graph TD
    InputA["Bit A: 1"] & InputB["Bit B: 1"] --> XORGate["Gerbang XOR: A ^ B"]
    InputA & InputB --> ANDGate["Gerbang AND: A & B"]
    XORGate --> SumOutput["Bit Jumlah (Sum S): 0"]
    ANDGate --> CarryOutput["Bit Bawaan (Carry C): 1"]
```
Arsitektur penambahan di dalam ALU (Arithmetic Logic Unit):
- **Ripple Carry Adder (RCA)**: Carry merambat serial dari bit 0 ke bit 31, menimbulkan latensi perambatan gerbang $O(N)$.
- **Carry-Lookahead Adder (CLA)**: Menghitung bit carry secara paralel dalam waktu $O(\log N)$ menggunakan generator $G_i = A_i \cdot B_i$ dan propagator $P_i = A_i \oplus B_i$.
""",
        "code_block": '''def base_converter(number: int, base: int) -> str:
    """
    Mengonversi bilangan bulat desimal positif ke basis b (2 s/d 16).
    """
    if number == 0:
        return "0"
    digits = "0123456789ABCDEF"
    result = []
    val = number
    while val > 0:
        remainder = val % base
        result.append(digits[remainder])
        val //= base
    return "".join(reversed(result))

decimal_val = 254
bin_str = base_converter(decimal_val, 2)
hex_str = base_converter(decimal_val, 16)

print(f"Desimal : {decimal_val}")
print(f"Biner   : {bin_str} (Basis 2)")
print(f"Heksa   : 0x{hex_str} (Basis 16)")
''',
        "pitfalls": """
1. **Integer Overflow Siluman**: Menambahkan 1 pada bilangan unsigned 8-bit bernilai 255 menghasilkan 0 (`255 + 1 = 0`), menyebabkan bug sistem navigasi roket Ariane 5 hancur 37 detik pasca peluncuran.
2. **Endianness Confusion**: Menyimpan integer 32-bit `0x12345678` di memori Little-Endian menyimpannya sebagai byte urutan terbalik: `78 56 34 12`, membingungkan developer saat memeriksa heksadesimal mentah di debugger.
3. **Off-by-One Bit Shift**: Menggeser signed integer ke kanan (`>>`) mempertahankan bit tanda (Arithmetic Shift Right), bukan mengisi dengan 0 (Logical Shift Right).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Simulator Konverter Basis Interaktif
Tulis program yang menerima input integer desimal dan mencetak representasi Biner, Oktal, dan Heksadesimal tanpa menggunakan fungsi bawaan `bin()`, `oct()`, atau `hex()`.

### Tingkat 2 (Menengah) - Simulator 4-Bit Ripple Carry Adder
Bangun simulasi gerbang logika dasar (NOT, AND, OR, XOR) dalam kode perangkat lunak. Gabungkan untuk membentuk modul Half-Adder, Full-Adder, dan rangkai 4 buah Full-Adder untuk mensimulasikan penambahan dua bilangan 4-bit biner beserta bendera Overflow flag.

### Tingkat 3 (Mahir) - Implementasi Fixed-Point Q16.16 Arithmetic
Tulis pustaka aritmatika fixed-point format Q16.16 (16 bit bilangan bulat, 16 bit pecahan) dalam C atau Rust untuk mikrokontroler tanpa unit FPU hardware. Implementasikan operasi penjumlahan, perkalian, dan pembagian dengan deteksi overflow saturasi.

#### Rubrik Penilaian
- **40% Presisi Representasi Bit**: Tidak ada kesalahan carry atau pergeseran posisi digit.
- **30% Deteksi Kondisi Batas**: Mampu menangani signed overflow dan representasi Two's Complement.
- **30% Efisiensi Komputasi**: Menghindari operasi pembagian modulo lambat dengan bitwise mask (`& (2^k - 1)`) jika basis adalah pangkat dua.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [The Elements of Computing Systems (Nisan & Schocken)](https://www.nand2tetris.org/) | Buku terkenal Nand2Tetris membangun komputer modern dari gerbang logika. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.004 Computation Structures](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | Desain prosesor digital, hierarki memori, dan sistem instruksi biner MIT. |
| 🔬 Makalah Seminal | [A Symbolic Analysis of Relay and Switching Circuits (Claude Shannon, 1938)](https://doi.org/10.1109/EE.1938.6431064) | Tesis master paling berpengaruh yang menghubungkan aljabar Boolean dengan sirkuit elektronik. |
| 💻 Lab Interaktif | [Logic.ly Digital Logic Circuit Simulator](https://logic.ly/demo/) | Simulator gerbang logika interaktif drag-and-drop di browser web. |
"""
    },
    11: {
        "intuition": """
Bayangkan Anda memegang selembar kain karet elastis dua dimensi yang memiliki gambar lingkaran. Anda kemudian menarik kain karet tersebut ke arah horizontal 2x lipat dan membiarkan arah vertikal tetap. Gambar lingkaran Anda berubah menjadi elips lonjong.

Peristiwa ini disebut **Transformasi Linier**:
- Matriks adalah 'mesin' yang meregangkan, memutar, atau membalik ruang.
- Garis yang awalnya lurus akan tetap lurus setelah transformasi, dan titik pusat asal $(0, 0)$ tidak pernah berpindah.
- Garis yang arahnya sama persis sebelum dan sesudah peregangan (hanya panjangnya yang berubah) disebut **Eigenvector**, dan faktor perpanjangannya disebut **Eigenvalue**!

Seluruh grafik 3D di game modern, algoritma PageRank Google yang mencari miliaran halaman web, hingga model Transformer ChatGPT pada dasarnya adalah perkalian matriks aljabar linier masif.
[📚 Pelajari: 3Blue1Brown Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra)
""",
        "theory": r"""
### 11.1 Ruang Vektor & Transformasi Linier ([MIT 18.06 Gilbert Strang](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/))
Ruang vektor $V$ atas medan $\mathbb{F}$ memenuhi 8 aksioma penambahan vektor dan perkalian skalar. Transformasi $T: V \to W$ bersifat linier jika dan hanya jika:
$$T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v}) \quad \text{dan} \quad T(c\mathbf{u}) = cT(\mathbf{u})$$
Representasi matriks transformasi $\mathbf{A} \in \mathbb{R}^{m \times n}$ memetakan koordinat basis input ke basis output:
$$\mathbf{y} = \mathbf{A} \mathbf{x}$$

### 11.2 Nilai Eigen, Vektor Eigen & Dekomposisi Spektral ([Stanford EE263 Linear Dynamical Systems](https://web.stanford.edu/class/ee263/))
Vektor tak-nol $\mathbf{v}$ adalah vektor eigen dari $\mathbf{A}$ dengan nilai eigen $\lambda$ jika:
$$\mathbf{A} \mathbf{v} = \lambda \mathbf{v} \iff (\mathbf{A} - \lambda \mathbf{I}) \mathbf{v} = \mathbf{0}$$
Nilai $\lambda$ diperoleh dari penyelesaian persamaan karakteristik:
$$\det(\mathbf{A} - \lambda \mathbf{I}) = 0$$

### 11.3 Singular Value Decomposition (SVD) ([Gilbert Strang SVD Paper](https://doi.org/10.1137/1035028))
Setiap matriks riil $\mathbf{A} \in \mathbb{R}^{m \times n}$ dapat difaktorkan menjadi tiga matriks:
$$\mathbf{A} = \mathbf{U} \mathbf{\Sigma} \mathbf{V}^T$$
Di mana:
- $\mathbf{U} \in \mathbb{R}^{m \times m}$ adalah matriks ortogonal vektor singular kiri ($AA^T$).
- $\mathbf{\Sigma} \in \mathbb{R}^{m \times n}$ adalah matriks diagonal nilai singular $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$.
- $\mathbf{V} \in \mathbb{R}^{n \times n}$ adalah matriks ortogonal vektor singular kanan ($A^T A$).
Teorema Eckart-Young-Mirsky: Aproksimasi rank-$k$ terbaik untuk matriks $\mathbf{A}$ diperoleh dengan mempertahankan $k$ nilai singular pertama:
$$\mathbf{A}_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^T$$
""",
        "internals": """
```mermaid
graph LR
    InputVector["Vektor Input x"] --> RightSingular["Rotasi Basis Awal: V^T"]
    RightSingular --> Scaling["Peregangan Sumbu Koordinat: Matriks Diagonal Sigma"]
    Scaling --> LeftSingular["Rotasi Basis Akhir: U"]
    LeftSingular --> OutputVector["Vektor Hasil Transformasi y = A x"]
```
Pustaka komputasi numerik tingkat rendah:
- **BLAS (Basic Linear Algebra Subprograms)**:
  - Level 1: Operasi vektor-vektor ($y = \alpha x + y$) - $O(N)$
  - Level 2: Operasi matriks-vektor ($y = \alpha A x + \beta y$) - $O(N^2)$
  - Level 3: Operasi matriks-matriks ($C = \alpha A B + \beta C$) - $O(N^3)$ dioptimalkan via cache-blocking mikrokernel CPU register.
- **LAPACK**: Pustaka Fortran/C performa tinggi untuk faktorisasi LU, QR, Cholesky, dan dekomposisi eigen.
""",
        "code_block": '''import numpy as np

def low_rank_svd_approximation(matrix: np.ndarray, rank_k: int) -> np.ndarray:
    """
    Melakukan kompresi matriks dengan aproksimasi SVD rank-k optimal (Teorema Eckart-Young).
    """
    U, s, Vt = np.linalg.svd(matrix, full_matrices=False)
    # Potong hanya k komponen singular teratas
    U_k = U[:, :rank_k]
    s_k = s[:rank_k]
    Vt_k = Vt[:rank_k, :]
    
    # Rekonstruksi matriks terkompresi
    approx = np.dot(U_k * s_k, Vt_k)
    return approx

# Matriks data sintetis 5x5
np.random.seed(42)
original_mat = np.random.randn(5, 5)
compressed_rank2 = low_rank_svd_approximation(original_mat, rank_k=2)

frobenius_error = np.linalg.norm(original_mat - compressed_rank2, 'fro')
print(f"Matriks Asli: {original_mat[:2, :2].tolist()}")
print(f"Aproksimasi Rank-2: {compressed_rank2[:2, :2].tolist()}")
print(f"Galat Rekonstruksi Frobenius: {frobenius_error:.4f}")
''',
        "pitfalls": """
1. **Inverting Matrices Explicitly**: Menghitung invers langsung $\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$ dalam kode produksi alih-alih menggunakan penyelesai sistem linier `np.linalg.solve(A, b)` (faktorisasi LU/Cholesky), yang menyebabkan instabilitas numerik parah dan pembengkakan memori.
2. **Matrix Multiplication Non-commutativity**: Mengasumsikan $\mathbf{A}\mathbf{B} = \mathbf{B}\mathbf{A}$, padahal perkalian matriks tidak komutatif, mengakibatkan bug rotasi orientasi 3D terbalik.
3. **Ill-Conditioned Matrices**: Matriks dengan *condition number* sangat besar ($\kappa(\mathbf{A}) = \sigma_{\max} / \sigma_{\min} \gg 10^8$) menyebabkan error floating point kecil pada input teramplifikasi menjadi salah 100% pada solusi.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Visualisasi Transformasi Geometri 2D
Tulis skrip Python dengan Matplotlib yang menggambar sebuah persegi di koordinat $(0,0)$ s/d $(1,1)$. Kalikan titik-titik sudut persegi dengan matriks rotasi $\mathbf{R}(\theta)$ dan matriks geser (*shear*). Tunjukkan perubahan bentuk geometrisnya secara visual.

### Tingkat 2 (Menengah) - Implementasi Power Iteration untuk Eigenvalue Terbesar
Implementasikan algoritma iterasi daya (*Power Iteration*) untuk mencari eigenvalue dominan dan eigenvector terkait dari sebuah matriks simetris tanpa menggunakan `np.linalg.eig`. Buktikan konvergensi rasio Rayleigh.

### Tingkat 3 (Mahir) - Kompresi Citra Grayscale Menggunakan SVD
Muat sebuah gambar grayscale $512 \times 512$ piksel sebagai matriks riil. Lakukan faktorisasi SVD dan rekam ukuran penyimpanan citra dengan $k \in \{5, 20, 50, 100\}$. Plot grafik trade-off antara rasio kompresi data vs Mean Squared Error (MSE) citra rekonstruksi.

#### Rubrik Penilaian
- **40% Ketepatan Matematis**: Implementasi ortogonalisasi Gram-Schmidt atau faktorisasi SVD akurat.
- **30% Optimasi Performa**: Menggunakan operasi tervektorisasi NumPy/BLAS tanpa loop Python lambat.
- **30% Analisis Galat Numerik**: Mampu menghitung Frobenius norm dan residual error solusi linier.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Linear Algebra and Its Applications (Gilbert Strang)](https://math.mit.edu/~gs/) | Buku rujukan standar emas dunia pengantar aljabar linier intuitif dan aplikasi. |
| 🎓 Kuliah Terbuka | [MIT OCW 18.06 Linear Algebra (Gilbert Strang)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/) | Seri kuliah paling terkenal dalam sejarah matematika terapan MIT. |
| 🔬 Makalah Seminal | [The Anatomy of a Large-Scale Hypertextual Web Search Engine (Page & Brin, 1998)](http://infolab.stanford.edu/pub/papers/google.pdf) | Paper asli Google PageRank berbasis eigenvector Markov chain ruang dokumen. |
| 💻 Lab Interaktif | [3Blue1Brown Linear Transformations Interactive](https://www.3blue1brown.com/topics/linear-algebra) | Seri visualisasi interaktif transformasi ruang vektor dan determinan. |
"""
    },
    18: {
        "intuition": """
Bayangkan Anda seorang dokter yang sedang menguji obat penurun demam baru pada 100 pasien. Setelah diberi obat, 60 pasien sembuh dalam tempo 2 jam. Apakah obat Anda benar-benar ampuh berkhasiat? Atau jangan-jangan ke-60 orang itu sembuh sendiri secara kebetulan?

Anda tidak bisa memberikan obat ke seluruh 8 miliar manusia di bumi untuk memastikannya. Anda hanya memiliki sampel kecil.
**Statistika Inferensial** adalah seni mengambil keputusan rasional di bawah ketidakpastian: bagaimana menyimpulkan sifat seluruh populasi raksasa secara tepat hanya dari segelintir sampel data terbatas, lengkap dengan batas toleransi kesalahannya.
[📚 Pelajari: MIT Statistics for Applications](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/)
""",
        "theory": r"""
### 18.1 Estimasi Titik: Maximum Likelihood Estimation (MLE) ([MIT 18.650](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/))
Diberikan sampel independen berdistribusi identik (i.i.d.) $\mathbf{X} = \{x_1, \dots, x_n\}$ dari distribusi dengan parameter $\theta$. Fungsi likelihood:
$$L(\theta) = \prod_{i=1}^n f(x_i; \theta)$$
Fungsi log-likelihood:
$$\ell(\theta) = \ln L(\theta) = \sum_{i=1}^n \ln f(x_i; \theta)$$
Estimator MLE adalah nilai parameter $\hat{\theta}_{\text{MLE}}$ yang memaksimalkan $\ell(\theta)$:
$$\hat{\theta}_{\text{MLE}} = \arg\max_\theta \ell(\theta) \implies \left. \frac{\partial \ell(\theta)}{\partial \theta} \right|_{\hat{\theta}} = 0$$

### 18.2 Uji Hipotesis Neyman-Pearson & p-value ([NIST Engineering Statistics](https://www.itl.nist.gov/div898/handbook/))
- **Hipotesis Nol ($H_0$)**: Tidak ada efek (perbedaan murni kebetulan acak).
- **Hipotesis Alternatif ($H_1$)**: Terdapat efek riil signifikan.
Statistik uji $Z$ untuk uji beda dua rata-rata sampel besar:
$$Z = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}$$
- **p-value**: Probabilitas memperoleh statistik uji seekstrem atau lebih ekstrem dari yang teramati jika $H_0$ benar.
- Jika $p\text{-value} < \alpha$ (tingkat signifikansi, misal $\alpha = 0.05$), tolak $H_0$.
""",
        "internals": """
```mermaid
flowchart TD
    ExperimentDesign["Desain A/B Testing Terkontrol Acak"] --> SampleSplit["Pembagian Pengguna 50-50: Grup Kontrol A vs Varian B"]
    SampleSplit --> DataCollection["Pengumpulan Metrik Konversi & Retensi"]
    DataCollection --> StatisticalTest["Uji Hipotesis Dua Sisi: Two-Sample t-Test / Welch t-Test"]
    StatisticalTest --> PValueCalc["Hitung p-value & Confidence Interval 95%"]
    PValueCalc --> Decision{"Apakah p-value < 0.05 & Ukuran Efek Signifikan?"}
    Decision -- "Ya" --> Rollout["Tolak H0: Rollout Varian B ke 100% Pengguna"]
    Decision -- "Tidak" --> KeepControl["Gagal Tolak H0: Pertahankan Desain A (Cegah Degradasi)"]
```
Tipe Kesalahan Inferensial:
- **Tipe I Error ($\alpha$)**: *False Positive* — Menyimpulkan ada efek padahal sebenarnya tidak ada.
- **Tipe II Error ($\beta$)**: *False Negative* — Gagal mendeteksi efek yang sebenarnya nyata.
- **Statistical Power ($1 - \beta$)**: Kemampuan eksperimen untuk mendeteksi efek nyata dengan benar (standar industri: minimal 80%).
""",
        "code_block": '''import numpy as np
from scipy import stats

def ab_test_significance(control_conversions: int, control_total: int,
                         variant_conversions: int, variant_total: int,
                         alpha: float = 0.05) -> dict:
    """
    Melakukan uji signifikansi proporsi A/B testing dua populasi (Two-Proportion Z-Test).
    """
    p1 = control_conversions / control_total
    p2 = variant_conversions / variant_total
    
    # Proporsi gabungan di bawah asumsi H0 (p1 == p2)
    p_pool = (control_conversions + variant_conversions) / (control_total + variant_total)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / control_total + 1 / variant_total))
    
    z_stat = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat))) # Uji dua arah
    
    is_significant = p_value < alpha
    return {
        "control_rate": p1,
        "variant_rate": p2,
        "relative_uplift_pct": ((p2 - p1) / p1) * 100.0,
        "z_stat": z_stat,
        "p_value": p_value,
        "statistically_significant": is_significant
    }

res = ab_test_significance(control_conversions=450, control_total=10000,
                           variant_conversions=530, variant_total=10000)

print(f"Konversi Kontrol: {res['control_rate']*100:.2f}% | Varian: {res['variant_rate']*100:.2f}%")
print(f"Uplift: {res['relative_uplift_pct']:+.2f}% | p-value: {res['p_value']:.4f}")
print(f"Keputusan Signifikan: {res['statistically_significant']}")
''',
        "pitfalls": """
1. **p-Hacking & Early Peeking**: Memeriksa p-value setiap 10 menit saat eksperimen A/B testing berjalan dan menghentikan pengujian seketika saat $p < 0.05$, melipatgandakan *false positive rate* hingga 30-40%.
2. **Confusing Statistical Significance with Practical Significance**: Mengklaim kemenangan peningkatan waktu muat halaman 0.01ms sebagai 'sangat signifikan' karena sampel 10 juta pengguna, padahal dampaknya nol terhadap pengalaman pengguna.
3. **Survivor Bias (Bias Kesintasan)**: Hanya menganalisis pengguna yang tetap aktif di aplikasi dan menyimpulkan fitur baru disukai, mengabaikan fakta bahwa pengguna yang membenci fitur baru tersebut telah langsung uninstall.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Konstruksi Confidence Interval Bootstrap
Tulis skrip Python yang menerima array data numerik kecil ($N=30$) dan membuat interval kepercayaan 95% untuk rata-rata menggunakan metode *non-parametric bootstrapping* (10.000 kali resampling dengan pengembalian) tanpa asumsi distribusi normal.

### Tingkat 2 (Menengah) - Kalkulator Ukuran Sampel Minimum (Power Analysis)
Implementasikan fungsi untuk menghitung ukuran sampel minimum per variasi dalam A/B testing berdasarkan metrik dasar (*baseline conversion rate*), *Minimum Detectable Effect* (MDE), $\alpha = 0.05$, dan *Power* $(1-\beta) = 0.80$.

### Tingkat 3 (Mahir) - Uji Hipotesis Sekuensial Adaptif (mSPRT)
Rancang dan implementasikan algoritma *mixture Sequential Probability Ratio Test* (mSPRT) yang memungkinkan continuous monitoring A/B testing tanpa terkena penalti inflasi p-value uji ganda (*multiple testing problem*).

#### Rubrik Penilaian
- **40% Ketepatan Teori Probabilitas**: Formulasi hipotesis nol $H_0$ dan pengujian dua arah dieksekusi benar.
- **30% Kontrol Kesalahan Tipe I & II**: Mengatasi inflasi alpha pada pengujian berulang (*Bonferroni correction* atau *FDR*).
- **30% Validitas Komputasi Statistik**: Perhitungan Z-score, t-distribution derajat kebebasan akurat.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Statistical Inference (Casella & Berger)](https://epdf.pub/statistical-inference-second-edition.html) | Kitab rujukan matematika statistik inferensial standar program pascasarjana. |
| 🎓 Kuliah Terbuka | [MIT OCW 18.650 Statistics for Applications](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/) | Estimasi parametrik, non-parametrik, MLE, Bayesian, dan pengujian hipotesis. |
| 🔬 Makalah Seminal | [The Probable Error of a Mean ("Student" / W.S. Gosset, 1908)](https://doi.org/10.2307/2331554) | Paper pendiri distribusi t-Student yang melahirkan statistika sampel kecil. |
| 💻 Lab Interaktif | [Seeing Theory: A Visual Introduction to Probability and Statistics](https://seeing-theory.brown.edu/) | Situs visualisasi interaktif dari Brown University untuk inferensi statistik. |
"""
    },
    19: {
        "intuition": """
Bayangkan seekor semut berjalan di atas lantai ubin. Setiap detik, ia melempar koin: kepala melangkah ke ubin depan, ekor melangkah ke ubin belakang. Di mana posisi semut setelah 1.000 detik?

Anda tidak bisa memprediksi lokasi pasti semut karena gerakannya acak. Namun, Anda bisa memprediksi **distribusi kemungkinan** keberadaannya: semut kemungkinan besar masih berada di dekat titik awal, dan sangat mustahil berada 1.000 ubin jauhnya!

Inilah **Proses Stokastik & Rantai Markov**:
Model matematika untuk sistem yang berevolusi seiring waktu di bawah pengaruh keacakan. Keajaiban sifat Markov adalah: **Masa depan hanya bergantung pada keadaan Anda saat ini, bukan pada sejarah masa lalu Anda**.
[📚 Pelajari: Markov Chains Visual Interactive](https://setosa.io/ev/markov-chains/)
""",
        "theory": r"""
### 19.1 Rantai Markov Waktu Diskrit (DTMC) & Sifat Markov ([MIT 6.041 Probabilistic Systems](https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/))
Barisan variabel acak $\{X_n, n \ge 0\}$ dengan ruang keadaan diskrit $S$ memenuhi **Sifat Markov** jika:
$$P(X_{n+1} = j \mid X_n = i, X_{n-1} = i_{n-1}, \dots, X_0 = i_0) = P(X_{n+1} = j \mid X_n = i) = P_{ij}$$
Matriks probabilitas transisi satu langkah $\mathbf{P} = [P_{ij}]$ memenuhi:
$$P_{ij} \ge 0, \quad \sum_{j \in S} P_{ij} = 1$$

### 19.2 Distribusi Stasioner & Teorema Ergodi ([Ross Stochastic Processes](https://www.wiley.com/en-us/Stochastic+Processes%2C+2nd+Edition-p-9780471120629))
Distribusi probabilitas $\boldsymbol{\pi}$ disebut stasioner jika:
$$\boldsymbol{\pi} \mathbf{P} = \boldsymbol{\pi}, \quad \text{dengan} \quad \sum_{i} \pi_i = 1$$
Jika rantai Markov bersifat *irreducible* (semua keadaan saling terhubung) dan *aperiodik*, maka distribusi probabilitas keadaan konvergen ke distribusi stasioner unik tak peduli keadaan awal:
$$\lim_{n \to \infty} P(X_n = j \mid X_0 = i) = \pi_j$$

### 19.3 Proses Poisson & Gerak Brown (Wiener Process) ([Stanford Stats](https://web.stanford.edu/class/stats217/))
- **Proses Poisson**: Menghitung kedatangan peristiwa acak berkecepatan rata-rata $\lambda$:
  $$P(N(t) = k) = \frac{(\lambda t)^k e^{-\lambda t}}{k!}$$
- **Gerak Brown (Wiener Process $W_t$)**:
  1. $W_0 = 0$
  2. Inkrement independen: $W_t - W_s \sim \mathcal{N}(0, t - s)$ untuk $t > s$.
  3. Trayektori kontinu di mana-mana tetapi tidak terdiferensiasi di titik mana pun.
""",
        "internals": """
```mermaid
stateDiagram-v2
    direction LR
    StateA: Server Sehat
    StateB: Server Overload
    StateC: Server Crash

    StateA --> StateA: P_AA = 0.90
    StateA --> StateB: P_AB = 0.08
    StateA --> StateC: P_AC = 0.02
    
    StateB --> StateA: P_BA = 0.30 (Recover)
    StateB --> StateB: P_BB = 0.50
    StateB --> StateC: P_BC = 0.20
    
    StateC --> StateA: P_CA = 0.99 (Reboot Auto)
    StateC --> StateC: P_CC = 0.01
```
Alur eksekusi internal simulasi Markov:
1. **Representasi Matriks Sparse**: Digunakan untuk graf keadaan dengan jutaan node (PageRank).
2. **Markov Chain Monte Carlo (MCMC)**: Menggunakan algoritma Metropolis-Hastings untuk mengambil sampel dari distribusi posterior berdimensi tinggi dalam fisika statistik dan machine learning.
""",
        "code_block": '''import numpy as np

def calculate_stationary_distribution(transition_matrix: np.ndarray) -> np.ndarray:
    """
    Menghitung distribusi stasioner pi dari matriks transisi P via pemecahan sistem linier.
    pi * P = pi  <=>  pi * (P - I) = 0, dengan sum(pi) = 1
    """
    n = transition_matrix.shape[0]
    # Ubah sistem persamaan: gantikan persamaan terakhir dengan kondisi normalisasi
    A = transition_matrix.T - np.eye(n)
    A[-1] = np.ones(n)
    b = np.zeros(n)
    b[-1] = 1.0
    
    pi = np.linalg.solve(A, b)
    return pi

# Matriks transisi cuaca: [Cerah, Hujan, Berawan]
P = np.array([
    [0.70, 0.10, 0.20],
    [0.25, 0.50, 0.25],
    [0.30, 0.30, 0.40]
])

pi = calculate_stationary_distribution(P)
print(f"Peluang Stasioner Jangka Panjang:")
print(f"Cerah   : {pi[0]*100:.2f}%")
print(f"Hujan   : {pi[1]*100:.2f}%")
print(f"Berawan : {pi[2]*100:.2f}%")
''',
        "pitfalls": """
1. **Assuming Memorylessness for Processes with Deep State**: Mengasumsikan sistem antrian server adalah Markovian murni (Poisson), padahal latensi tail request sangat bergantung pada ukuran cache yang terisi dari request-request sebelumnya.
2. **Periodicity Trap**: Mencoba menghitung limit $\mathbf{P}^n$ pada rantai Markov periodik (misal partikel berosilasi bolak-balik antara keadaan 0 dan 1), di mana limit tidak pernah konvergen.
3. **Absorbing State Oversight**: Tidak mendeteksi adanya absorbing state (keadaan yang jika dimasuki tidak bisa ditinggalkan, seperti kondisi `Crash` permanen), yang membuat probabilitas stasioner keadaan lain runtuh menjadi nol.
""",
        "exercises": """
### Tingkat 1 (Pemula) - Generator Teks Berbasis Rantai Markov
Tulis skrip Python yang membaca korpus teks buku pendek, membangun matriks frekuensi transisi kata berorde-1 ($P(w_{t+1} \mid w_t)$), dan membangkitkan paragraf teks acak 50 kata baru secara probabilistik.

### Tingkat 2 (Menengah) - Simulasi Teori Antrian M/M/1
Simulasikan sistem antrian server tunggal model M/M/1 (kedatangan Poisson $\lambda$, waktu pelayanan eksponensial $\mu$). Plot rata-rata panjang antrian di memori server saat intensitas trafik $\rho = \lambda / \mu$ mendekati 1.0 ($100\%$ utilisasi) untuk membuktikan ledakan latensi hiperbolik $L = \frac{\rho}{1 - \rho}$.

### Tingkat 3 (Mahir) - Algoritma PageRank Berbasis Random Walk
Implementasikan algoritma PageRank pada graf web berisi 10.000 node menggunakan metode *Power Iteration* dengan *damping factor* $d = 0.85$. Tunjukkan bahwa penambahan teleportasi acak mengatasi masalah spider traps dan dead ends.

#### Rubrik Penilaian
- **40% Ketepatan Teori Stokastik**: Matriks transisi stokastik valid (jumlah baris tepat 1.0).
- **30% Analisis Konvergensi**: Mampu menguji konvergensi distribusi stasioner via eigenvalue dominan ($\lambda = 1$).
- **30% Validitas Simulasi**: Variabel waktu kedatangan dan transisi acak dimodelkan dengan generator pseudo-random yang tepat.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Introduction to Stochastic Processes (Lawler)](https://www.routledge.com/Introduction-to-Stochastic-Processes/Lawler/p/book/9781584886518) | Buku pengantar matematika proses stokastik dan rantai Markov yang sangat jernih. |
| 🎓 Kuliah Terbuka | [MIT OCW 6.041 Probabilistic Systems Analysis](https://ocw.mit.edu/courses/6-041-probabilistic-systems-analysis-and-applied-probability-fall-2010/) | Kuliah legendaris John Tsitsiklis mengenai probabilitas dan proses stokastik. |
| 🔬 Makalah Seminal | [The Theory of Queues with Applications to Automata (Kendall, 1953)](https://doi.org/10.1111/j.2517-6161.1953.tb00139.x) | Paper pendiri notasi sistem antrian Kendall (M/M/1, M/G/1). |
| 💻 Lab Interaktif | [Markov Chains Visualized (Victor Powell / Setosa)](https://setosa.io/ev/markov-chains/) | Simulasi interaktif graf transisi keadaan Markov berbasis web. |
"""
    },
    21: {
        "intuition": """
Ketikkan `0.1 + 0.2 == 0.3` di terminal bahasa pemrograman favorit Anda (Python, JavaScript, C). Hasilnya mengejutkan: **FALSE**! Mengapa? Karena di komputer Anda, `0.1 + 0.2` menghasilkan `0.30000000000000004`.

Komputer memiliki memori berhingga: ia tidak bisa menyimpan angka pecahan tak hingga seperti $\\pi$ atau sepertiga ($1/3 = 0.3333\\dots$). Segala perhitungan di dunia nyata (lintasan roket, rendering 3D, simulasi fluida pesawat, penentuan harga saham) adalah **aproksimasi terpotong**.
**Metode Numerik & Analisis Galat** adalah seni menghitung solusi matematika kompleks secara komputasional dengan tetap mengendalikan galat agar tidak meledak dan menghancurkan sistem.
[📖 Pelajari: What Every Computer Scientist Should Know About Floating-Point](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html)
""",
        "theory": r"""
### 21.1 Standar Titik Kambang IEEE 754 & Analisis Galat ([IEEE 754 Standard](https://ieeexplore.ieee.org/document/8766229))
Representasi floating-point biner presisi ganda (Float64 / Double Precision 64-bit):
- 1 bit tanda ($s$)
- 11 bit eksponen bias ($e$)
- 52 bit fraksi / mantissa ($m$)
$$x = (-1)^s \times 2^{e - 1023} \times (1.m_1 m_2 \dots m_{52})$$
Presisi mesin (*Machine Epsilon* $\varepsilon_m$): jarak terkecil antara 1.0 dan angka terdekat berikutnya di representasi hardware. Untuk IEEE 754 float64:
$$\varepsilon_m = 2^{-52} \approx 2.22 \times 10^{-16}$$

### 21.2 Metode Pencarian Akar: Newton-Raphson & Konvergensi Kuadratik ([MIT 18.330 Numerical Analysis](https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/))
Mencari nilai $x$ sehingga $f(x) = 0$ menggunakan aproksimasi deret Taylor linier:
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$
Jika $f'(x^*) \neq 0$, metode ini memiliki orde konvergensi kuadratik ($p=2$):
$$|e_{n+1}| \le C |e_n|^2$$
Jumlah digit desimal presisi berlipat ganda di setiap iterasi tunggal!

### 21.3 Integrasi Numerik & Kuadratur Gauss ([Burden & Faires Numerical Analysis](https://cengage.com/))
- Metode Trapesium Komposit: Galat pemotongan $O(h^2)$.
- Metode Simpson 1/3 Komposit: Mengaproksimasi kurva dengan parabola kuadratik:
$$\int_a^b f(x) dx \approx \frac{h}{3} \sum_{i=0}^{n/2 - 1} \left[ f(x_{2i}) + 4f(x_{2i+1}) + f(x_{2i+2}) \right]$$
Galat pemotongan Simpson adalah $O(h^4)$, meluruh sangat cepat seiring bertambahnya partisi langkah $h$.
""",
        "internals": """
```mermaid
graph TD
    FunctionInput["Fungsi f(x) dan Titik Awal x_0"] --> Tangent["Hitung Garis Singgung di f(x_n) dengan Gradien f'(x_n)"]
    Tangent --> XIntercept["Hitung Titik Potong Sumbu-X: x_(n+1) = x_n - f(x_n)/f'(x_n)"]
    XIntercept --> ResidualCheck{"Apakah |f(x_(n+1))| < Toleransi Epsilon?"}
    ResidualCheck -- "Tidak" --> Tangent
    ResidualCheck -- "Ya" --> RootOutput["Akar Solusi Ditemukan Presisi Tinggi (Konvergensi Kuadratik)"]
```
Sumber Utama Galat Numerik:
1. **Truncation Error**: Galat akibat memotong deret matematika tak hingga menjadi deret berhingga.
2. **Round-off Error**: Galat akibat pembulatan representasi bit registers CPU.
3. **Catastrophic Cancellation**: Terjadi ketika dua angka yang nilainya hampir sama dikurangkan satu sama lain, melenyapkan bit-bit signifikan mantissa secara instan.
""",
        "code_block": '''def newton_raphson_solver(func, dfunc, x0: float, tol: float = 1e-12, max_iter: int = 100):
    """
    Penyelesai akar persamaan non-linier menggunakan metode Newton-Raphson presisi tinggi.
    """
    x = x0
    for iteration in range(1, max_iter + 1):
        fx = func(x)
        dfx = dfunc(x)
        if abs(dfx) < 1e-15:
            raise ZeroDivisionError("Turunan mendekati nol: singularitas numerik!")
        
        step = fx / dfx
        x -= step
        
        if abs(step) < tol:
            return x, iteration, abs(func(x))
            
    raise RuntimeError("Gagal konvergen dalam batas iterasi maksimum.")

# Kasus: Mencari akar kuadrat dari 2 -> f(x) = x^2 - 2 = 0
f = lambda x: x**2 - 2.0
df = lambda x: 2.0 * x

root, iters, residual = newton_raphson_solver(f, df, x0=1.0)
print(f"Akar terhitung  : {root:.16f}")
print(f"Nilai riil sqrt : {2.0**0.5:.16f}")
print(f"Konvergen dalam : {iters} iterasi (Residual: {residual:.2e})")
''',
        "pitfalls": """
1. **Catastrophic Cancellation in Quadratic Formula**: Menghitung $(-b + \sqrt{b^2 - 4ac}) / 2a$ saat $b > 0$ dan $b^2 \gg 4ac$, menyebabkan pengurangan dua angka yang hampir identik. Solusi stabil: gunakan bentuk alternatif $2c / (-b - \sqrt{b^2 - 4ac})$.
2. **Infinite Loops from Float Equality**: Menulis loop termination `while x != 1.0: x += 0.1` yang tidak pernah berhenti karena penambahan desimal $0.1$ pada floating point biner tidak pernah presisi tepat $1.0$.
3. **Runge Phenomenon in High-Order Polynomials**: Melakukan interpolasi polinomial derajat tinggi pada titik ekuidistan yang memicu osilasi liar di dekat ujung domain. Solusi: gunakan simpul Chebyshev (*Chebyshev nodes*).
""",
        "exercises": """
### Tingkat 1 (Pemula) - Deteksi Pembatalan Bencana (Catastrophic Cancellation)
Tulis skrip Python yang mengevaluasi fungsi $f(x) = \frac{1 - \cos(x)}{x^2}$ untuk nilai $x$ yang sangat kecil ($x = 10^{-1}, 10^{-3}, 10^{-7}, 10^{-9}$). Tunjukkan titik di mana formula naif kehilangan seluruh digit signifikannya dan bandingkan dengan aproksimasi deret Taylor: $f(x) \approx \frac{1}{2} - \frac{x^2}{24}$.

### Tingkat 2 (Menengah) - Integrator Adaptif Simpson (Adaptive Quadrature)
Implementasikan algoritma integrasi numerik adaptif Simpson yang membagi sub-interval secara otomatis hanya pada wilayah kurva fungsi yang memiliki osilasi/kelengkungan tinggi, sehingga menghemat komputasi pada wilayah fungsi yang datar.

### Tingkat 3 (Mahir) - Penyelesai Persamaan Diferensial Kaku (Stiff ODE Solver)
Implementasikan metode Runge-Kutta eksplisit orde-4 (RK4) dan metode implisit Backward Euler untuk menyelesaikan sistem persamaan diferensial kaku (*stiff system*): $y' = -1000y + 1000$. Tunjukkan bagaimana RK4 meledak menjadi tak hingga jika ukuran langkah $h > 2/1000$, sedangkan metode implisit tetap stabil tanpa syarat (*A-stable*).

#### Rubrik Penilaian
- **40% Stabilitas Numerik**: Algoritma tidak meledak pada kondisi batas dan mampu menghindari catastrophic cancellation.
- **30% Analisis Orde Konvergensi**: Mampu memvalidasi bahwa rasio penurunan galat sesuai dengan eksponen teoritis $O(h^p)$.
- **30% Penanganan Toleransi Presisi**: Penghentian iterasi berbasis perbandingan $\varepsilon$ yang aman tanpa perbandingan floating-point biner ketat `==`.
""",
        "references": """
| Kategori | Judul Sumber & Tautan Langsung | Deskripsi Singkat |
|---|---|---|
| 📖 Buku Teks | [Numerical Analysis (Burden & Faires)](https://cengage.com/) | Buku teks komprehensif analisis numerik, stabilitas solusi, dan algoritma. |
| 🎓 Kuliah Terbuka | [MIT OCW 18.330 Introduction to Numerical Analysis](https://ocw.mit.edu/courses/18-330-introduction-to-numerical-analysis-spring-2012/) | Metode aproksimasi, interpolasi, pencarian akar, dan persamaan diferensial. |
| 🔬 Makalah Seminal | [What Every Computer Scientist Should Know About Floating-Point Arithmetic (Goldberg, 1991)](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) | Makalah esensial acuan industri tentang presisi dan galat IEEE 754. |
| 💻 Lab Interaktif | [Floating Point Visually Explained (Float Toy)](https://evanw.github.io/float-toy/) | Visualisator interaktif representasi bit sign, exponent, dan mantissa IEEE 754. |
"""
    }
}
