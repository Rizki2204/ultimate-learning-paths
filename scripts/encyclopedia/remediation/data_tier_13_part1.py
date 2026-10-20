# -*- coding: utf-8 -*-
r"""
Authentic Remediation Data for Tier 13 Part 1 (Topics 196-201):
Cognitive Science Foundations, Computational Neuroscience & SNN, Neuroengineering & BCI,
Bioinformatics & Computational Biology, Cognitive Psychology & Mind Architecture, Formal Linguistics & Parsing.
"""

DATA_TIER_13_PART1 = {
    196: {
        "trace": r"""#### Tabel Penelusuran Inferensi Logika Simbolik & Keruntuhan Masalah Bingkai (Frame Problem)
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Ingest Fakta Awal | Proposisi: `Kucing(Mimi) \land Masuk(Mimi, Kotak)` | Evaluasi Basis Pengetahuan Orde Pertama | Tabel memori unifikasi simbolik termuat | Distribusi kepastian deterministik: $1.0$ | Sistem menyimpulkan: `DiDalam(Mimi, Kotak)` |
| 2. Perubahan Aksi Dunia | Aksi Fisik: `Pindah(Meja, RuangTamu)` | Sistem pakar mencoba memperbarui status dunia | Masalah Bingkai: Perlu aksi mengecek jutaan fakta statis | Logika deduksi mengevaluasi 100.000 aksioma | Beban komputasi inferensi meledak |
| 3. Injeksi Premis Kontradiktif | Fakta Inkonsisten: `Mimi(Hidup) \land Mimi(Mati)` | Kontradiksi masuk ke basis pengetahuan (Cyc/MYCIN) | Resolvent menghasilkan premis kosong kontradiktif: $P \land \neg P$ | Prinsip *Ex Falso Quodlibet* terpicu | Sistem logika kehilangan daya diskriminasi kebenaran |
| 4. Ledakan Penarikan Kesimpulan | Sembarang Teorema: `PresidenAdalahRobot()` | Dari kontradiksi, sembarang kesimpulan terbukti sah ($A \land \neg A \vdash B$) | Tumpukan penalaran simbolik meluap | Logika runtuh ke status *Explosion* | Sistem pakar membuktikan fakta absurd sebagai fakta sah |
| 5. Mitigasi Logika Non-Monotonik | Logika Default Reiter / Sirkumsripsi | Pembatasan inferensi melalui asumsi dunia tertutup (CWA) | Aturan defeasible: Asumsi dapat dibatalkan saat ada anomali | Derajat keyakinan probabilitas Bayesian diterapkan | Inferensi simbolik stabil dan tangguh terhadap noise |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Sistem Pakar Medis MYCIN & Masalah Bingkai AI Simbolik (GOFAI) (1980-an)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada era musim dingin kecerdasan buatan kedua (*Second AI Winter*) pada akhir 1980-an, proyek-proyek ambisius kecerdasan buatan simbolik klasik (*Good Old-Fashioned AI / GOFAI*) seperti sistem pakar diagnosis infeksi darah MYCIN (Stanford) dan basis pengetahuan akal sehat raksasa Cyc mengalami kegagalan adopsi di dunia nyata setelah menelan dana riset ratusan juta dolar.
- **Akar Masalah Rekayasa AI Simbolik & Kerapuhan Logika Deduktif**: Sistem pakar klasik mengandalkan ribuan aturan produksi diskret (*If-Then Production Rules*) dan logika predikat orde pertama (*First-Order Predicate Logic*). Sistem ini mengalami dua keruntuhan komputasional fatal: (1) **Masalah Bingkai (The Frame Problem)**: sistem tidak mampu memodelkan apa yang *tidak berubah* ketika suatu aksi terjadi di dunia nyata tanpa menuliskan aksioma pembatas secara eksplisit untuk setiap entitas, memicu ledakan kombinatorial pencarian; (2) **Kerapuhan Monotonik (Brittleness & Ex Falso Quodlibet)**: dalam logika deduktif murni, satu saja fakta medis atau aturan yang kontradiktif dimasukkan ke dalam basis pengetahuan, prinsip ledakan logika (*Principle of Explosion*) menyebabkan sistem secara valid membuktikan kebenaran proposisi apa pun yang absurd (misalnya menyimpulkan bahwa pasien dengan flu ringan harus segera diamputasi). Ketiadaan pemodelan ketidakpastian numerik kontinu menghancurkan kelangsungan sistem pakar di lingkungan klinis nyata.""",
            "snippet": r"""```python
# Analisis Kerapuhan Logika Simbolik Monotonik: Prinsip Ledakan (Ex Falso Quodlibet)
class SymbolicInferenceEngine:
    def __init__(self):
        self.knowledge_base = set()
        
    def add_fact(self, fact):
        self.knowledge_base.add(fact)
        
    def query(self, proposition):
        # Jika terdapat premis kontradiktif P dan NOT P di dalam sistem:
        has_contradiction = any((f"NOT_{f}" in self.knowledge_base) for f in self.knowledge_base)
        
        if has_contradiction:
            # PRINSIP LEDAKAN: Dari kontradiksi, SEMBARANG teorema dapat dibuktikan sah!
            # A and NOT A ==> B (Ex Falso Sequitur Quodlibet)
            return True # Menghasilkan kesimpulan fatal tanpa dasar medis!
            
        return proposition in self.knowledge_base

# MITIGASI MODERN: Jaringan Bayesian Probabilistik (Soft Probabilistic Inference)
class BayesianDiagnosticNode:
    def __init__(self, prior_prob):
        self.prob = prior_prob
        
    def update_evidence(self, likelihood_ratio):
        # Pembaruan aturan Bayes kontinu: Tidak pernah menghasilkan probabilitas 0 atau 1 mutlak
        odds = (self.prob / (1.0 - self.prob)) * likelihood_ratio
        self.prob = odds / (1.0 + odds)
        return self.prob # Stabil terhadap bukti yang saling bertentangan
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Runtuhnya GOFAI memicu lahirnya paradigma AI modern berbasis probabilitas dan koneksionisme: (1) Penggantian logika simbolik biner dengan **Probabilistic Graphical Models (Bayesian Networks)** yang dipelopori oleh Judea Pearl untuk menangani ketidakpastian klinis; (2) Transisi dari aturan buatan tangan (*Hand-Crafted Rules*) ke representasi fitur kontinu terdistribusi (*Distributed Neural Representations*); (3) Penerapan **Neuro-Symbolic AI** yang menggabungkan kemampuan penalaran terstruktur logika graf dengan ketahanan terhadap derau dari deep learning."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun mesin inferensi Forward Chaining sederhana dalam Python yang mengevaluasi basis pengetahuan aturan produksi (*Production Rules*): `IF A AND B THEN C`. Sistem menerima fakta awal dan secara iteratif menurunkan fakta baru hingga tidak ada lagi aturan yang dapat diaktifkan.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan fakta dalam struktur data `set`.
  - Representasikan aturan sebagai objek tuple: `(conditions_list, conclusion)`.
  - Lacak loop penarikan kesimpulan agar tidak terjadi penambahan berulang (*idempotent evaluation*).
- **Test Vector & Kasus Uji**:
  - Fakta: `{"Demam", "BintikMerah"}`.
  - Aturan: `IF Demam AND BintikMerah THEN Campak`, `IF Campak THEN IsolasiMandiri`.
  - Sistem harus menurunkan fakta akhir: `{"Demam", "BintikMerah", "Campak", "IsolasiMandiri"}`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Forward chaining presisi, loop konvergen rapi, penanganan kondisi majemuk benar.
  - Skor 50%: Bekerja untuk aturan satu kondisi namun gagal mengevaluasi konjungsi logika multi-kondisi (`AND`).
  - Skor 0%: Terjebak dalam infinite loop saat evaluasi aturan sirkular.

### Tingkat 2: Menengah
- **Tugas**: Bangun model Jaringan Bayesian 3-simpul sederhana (Hujan $\to$ Rumput Basah $\leftarrow$ Penyiram Taman) dalam Python murni: Hitung probabilitas posterior bersyarat $P(\text{Hujan} = \text{True} \mid \text{Rumput Basah} = \text{True})$ menggunakan inferensi eksak enumerasi probabilitas bersama (*Joint Probability Distribution*).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan Conditional Probability Tables (CPT) untuk setiap simpul graf.
  - Implementasikan formula Bayes: $P(A \mid B) = \frac{\sum_C P(A, B, C)}{\sum_{A, C} P(A, B, C)}$.
  - Tunjukkan fenomena *Explaining Away*: jika diketahui bahwa Penyiram Taman aktif, probabilitas bersyarat Hujan harus menurun.
- **Test Vector & Kasus Uji**:
  - Masukkan nilai CPT standar Pearl.
  - Nilai posterior $P(\text{Hujan} \mid \text{Rumput Basah})$ harus bernilai $\approx 0.357$, dan turun menjadi $\approx 0.104$ saat bukti $\text{Penyiram} = \text{True}$ ditambahkan.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Enumerasi probabilitas gabungan presisi, pembuktian efek explaining away akurat.
  - Skor 50%: Perhitungan benar namun salah menormalisasi pembagi marginal pada formula Bayes.
  - Skor 0%: Mengalikan probabilitas independen secara naif tanpa memperhitungkan relasi bersyarat.

### Tingkat 3: Mahir
- **Tugas**: Rancang arsitektur Neuro-Symbolic mini (Differentiable Inductive Logic Programming) dalam PyTorch: Bangun representasi predikat logika kontinu di mana operasi `AND` dimodelkan sebagai t-norm Gödel atau perkalian probabilitas lunak ($x \cdot y$), dan operasi `OR` dimodelkan sebagai t-conorm ($x + y - x y$). Latih matriks bobot aturan menggunakan optimasi gradien backpropagation.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan fakta sebagai matriks relasi biner kontinu berukuran $N \times N$.
  - Implementasikan operasi komposisi relasi logika lunak via perkalian matriks tensor: $R_{AC} = \sigma(R_{AB} \cdot R_{BC})$.
  - Loss function: Binary Cross-Entropy terhadap relasi target yang ingin dipelajari (misal relasi silsilah keluarga `Kakek(X, Y) \leftarrow Ayah(X, Z) \land Ayah(Z, Y)`).
- **Test Vector & Kasus Uji**:
  - Berikan fakta relasi graf keluarga 10 individu.
  - Model harus mampu mempelajari aturan relasi transitive multi-hop dengan akurasi prediksi $> 95\%$ dan bobot aturan yang dapat diinterpretasikan secara simbolik ($W > 0.90$).
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Differentiable logic t-norm presisi, konvergensi gradien stabil, interpretasi aturan terbukti.
  - Skor 50%: Model bekerja namun menggunakan neural network black-box tanpa pemodelan t-norm terstruktur.
  - Skor 0%: Aliran gradien terputus akibat operasi logika diskret `bool`."""
    },
    197: {
        "trace": r"""#### Tabel Penelusuran Siklus Dinamika SNN STDP & Ledakan Badai Epileptik Runaway Potentiation
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Inisialisasi Populasi Neuron | 10.000 Neuron Leaky Integrate-and-Fire | Potensial membran istirahat: $V_{\text{rest}} = -70\text{ mV}$ | Matriks sinaptik $W \in \mathbb{R}^{10k \times 10k}$ terisi bobot acak | Threshold penembakan: $V_{\text{th}} = -55\text{ mV}$ | Simulasi SNN dimulai pada laju penembakan 5 Hz |
| 2. Stimulasi Input Sensorik | Pulsa Arus Input Eksternal $I_{\text{inj}}$ | Integrasi membran: $\tau_m \frac{dV}{dt} = -(V - V_{\text{rest}}) + R I$ | Spike neuron presinaptik terdeteksi pada $t_{\text{pre}} = 10.2\text{ ms}$ | Neuron memancarkan spike aksi $\delta(t)$ | Potensial aksi merambat ke neuron pascasinaptik |
| 3. Aturan Plastisitas STDP Naif | Beda Waktu: $\Delta t = t_{\text{post}} - t_{\text{pre}} > 0$ | Peningkatan bobot sinaptik: $\Delta w = A_+ e^{-\Delta t / \tau_+}$ | Bobot sinaptik dinaikkan secara berulang tanpa batas atas | Ketiadaan batas saturasi bobot ($w \to \infty$) | Fenomena Long-Term Potentiation (LTP) tak terbatas |
| 4. Badai Epileptik Runaway | Seluruh 10.000 Neuron Menembak Serempak | Loop umpan balik rekuren eksitatori tak terkendali | Matriks bobot $W$ melipatgandakan arus eksitasi | Laju penembakan melonjak dari 5 Hz ke 350 Hz instan | Sinkronisasi patologis masif melumpuhkan simulator SNN! |
| 5. Mitigasi Penskalaan Homeostatis | Penstabilan Bobot Homeostatik | $w \leftarrow w \cdot \frac{r_{\text{target}}}{r_{\text{current}}}$ + Bounded Clamping $[0, w_{\max}]$ | Normalisasi total bobot sinaptik per dendrit | Populasi neuron kembali ke ritme Poisson asinkron | Jaringan SNN stabil, hemat energi, dan mampu belajar pola baru |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ledakan Badai Epileptik Runaway Potentiation pada Simulator SNN Komputasional (Brian2/NEST)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam pemodelan jaringan saraf tiruan berdenyut (*Spiking Neural Networks / SNN*) pada simulator neurosains komputasional skala besar (seperti Brian2, NEST, atau Human Brain Project) sepanjang dekade 2010-an, para peneliti neuroengineering berulang kali menghadapi fenomena bencana simulasi di mana populasi puluhan ribu neuron yang disimulasikan tiba-tiba meledak menjadi badai penembakan sinkron frekuensi tinggi (*runaway epileptic-like seizure*).
- **Akar Masalah Dinamika Saraf & Ketiadaan Regulasi Homeostatis**: Dalam biologi saraf nyata, plastisitas sinaptik yang bergantung pada waktu denyut (*Spike-Timing-Dependent Plasticity / STDP*) memperkuat koneksi sinapsis ($\text{LTP}$) jika neuron presinaptik menembak sesaat sebelum neuron pascasinaptik. Namun, jika aturan STDP diimplementasikan dalam kode simulasi tanpa mekanisme penyeimbang homeostatik (*Homeostatic Synaptic Scaling*) dan pemotongan bobot ketat ($w \in [0, w_{\max}]$), terjadi loop umpan balik positif katastropik: sinapsis yang menguat membuat neuron berikutnya menembak lebih cepat, yang pada gilirannya memicu penguatan STDP lebih lanjut. Dalam hitungan ratusan milidetik simulasi, seluruh populasi neuron terjerumus ke dalam osilasi sinkron hipereksitabilitas, mengonsumsi seluruh memori simulasi dan menghentikan proses komputasi neuromorfik.""",
            "snippet": r"""```python
# Analisis Cacat Plastisitas Sinaptik: STDP Liar vs Penskalaan Sinaptik Homeostatis
import numpy as np

# MODEL STDP CACAT: Peningkatan bobot tanpa batas atas (Unbounded LTP)
def flawed_stdp_update(w, dt, A_plus=0.01, tau_plus=20.0):
    if dt > 0: # Neuron presinaptik menembak sebelum pascasinaptik
        dw = A_plus * np.exp(-dt / tau_plus)
        w += dw # CACAT FATAL: Bobot terus bertambah menuju tak hingga!
        # Memicu RUNAWAY POTENTIATION dan badai epileptik sinkron!
    return w

# MITIGASI AMAN: Multiplicative STDP + Penskalaan Homeostatik (Turrigiano et al.)
def homeostatic_stdp_update(w, dt, current_firing_rate, target_firing_rate=5.0, w_max=1.0):
    if dt > 0:
        # Peningkatan bobot multiplicative (mengecil saat mendekati w_max)
        dw = 0.01 * (w_max - w) * np.exp(-dt / 20.0)
        w += dw
    elif dt < 0:
        # Penurunan bobot (LTD)
        dw = 0.012 * w * np.exp(dt / 20.0)
        w -= dw
        
    # Penskalaan Homeostatis: Jika laju penembakan terlalu tinggi, turunkan bobot secara merata
    homeostatic_factor = 1.0 + 0.001 * (target_firing_rate - current_firing_rate)
    w = np.clip(w * homeostatic_factor, 0.0, w_max)
    return w
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Pemahaman terhadap fenomena runaway potentiation merevolusi desain perangkat keras neuromorfik (Intel Loihi, IBM TrueNorth): (1) Penegakan wajib **Hard Weight Clamping** dan resolusi bobot diskret (misal presisi integer 8-bit $[0, 255]$); (2) Penerapan **Inhibitory Interneuron Balance (E/I Balance)** di mana setiap populasi neuron eksitatori diimbangi oleh neuron inhibitori (GABA-ergik) untuk meredam resonansi sinkron; (3) Integrasi mekanisme penyesuaian ambang batas dinamis (*Adaptive Spike Threshold*) yang menaikkan ambang letupan jika neuron menembak terlalu sering."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan simulator neuron Leaky Integrate-and-Fire (LIF) dari nol dalam Python menggunakan metode integrasi numerik Euler: Simulasikan dinamika tegangan membran $\tau_m \frac{dV}{dt} = -(V - V_{\text{rest}}) + R I(t)$ selama 100 milidetik dengan langkah waktu $dt = 0.1\text{ ms}$, hasilkan spike saat $V \ge V_{\text{th}}$, dan terapkan periode refraktori mutlak (*Refractory Period*) sebesar 2 milidetik.
- **Petunjuk Perancangan Arsitektur**:
  - Parameter: $V_{\text{rest}} = -70\text{ mV}, V_{\text{th}} = -55\text{ mV}, V_{\text{reset}} = -75\text{ mV}, \tau_m = 10\text{ ms}, R = 10\text{ M}\Omega$.
  - Selama periode refraktori pasca-spike, tahan tegangan membran pada $V_{\text{reset}}$ dan abaikan arus masukan $I(t)$.
- **Test Vector & Kasus Uji**:
  - Arus konstan sub-threshold ($I = 1.0\text{ nA}$): Tegangan membran mencapai kesetimbangan asimtotik tanpa memancarkan spike.
  - Arus supra-threshold ($I = 2.0\text{ nA}$): Neuron menembak secara teratur dengan frekuensi penembakan periodik $\approx 55\text{ Hz}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Integrasi numerik Euler presisi, mekanisme refraktori mutlak akurat, frekuensi penembakan sesuai analitis.
  - Skor 50%: Model bekerja namun lupa menerapkan periode refraktori sehingga tegangan berosilasi instan pada threshold.
  - Skor 0%: Mengabaikan suku kebocoran membran (menjadi Integrate-and-Fire murni tanpa leak).

### Tingkat 2: Menengah
- **Tugas**: Bangun simulasi jaringan saraf berdenyut (SNN) 100 neuron eksitatori dan 25 neuron inhibitori (E/I Network Dale's Principle) dalam Python/NumPy yang mengimplementasikan plastisitas STDP pada sinapsis eksitatori-ke-eksitatori. Buktikan stabilitas jaringan terhadap fenomena runaway potentiation dengan membandingkan dinamika laju penembakan dengan dan tanpa homeostatic scaling.
- **Petunjuk Perancangan Arsitektur**:
  - Matriks konektivitas sparse dengan probabilitas koneksi $p = 0.2$.
  - Terapkan aturan Dale: Neuron eksitatori hanya memancarkan bobot positif ($w > 0$), neuron inhibitori hanya memancarkan bobot negatif ($w < 0$).
  - Lacak rata-rata frekuensi penembakan populasi (*Population Firing Rate*) setiap 50 milidetik.
- **Test Vector & Kasus Uji**:
  - Tanpa homeostatis: Laju penembakan melonjak eksponensial ke $> 200\text{ Hz}$ dalam waktu $< 500\text{ ms}$.
  - Dengan homeostatic scaling: Laju penembakan stabil pada rentang target $10\text{ Hz} \pm 2\text{ Hz}$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi prinsip Dale presisi, homeostatic scaling terbukti menstabilkan laju penembakan.
  - Skor 50%: Model bekerja namun mengabaikan perbedaan dinamika sinapsis eksitatori vs inhibitori.
  - Skor 0%: Seluruh neuron menembak sinkron sempurna sejak iterasi pertama.

### Tingkat 3: Mahir
- **Tugas**: Rancang model pelatihan SNN berbasis Surrogate Gradient Backpropagation (seperti SLAYER / SuperSpike) dalam PyTorch: Karena fungsi pembentukan spike $\Theta(V - V_{\text{th}})$ memiliki turunan nol di mana-mana dan tak hingga di titik threshold (Dirac delta), gantikan turunan fungsi tangga tersebut pada backward pass dengan fungsi gradien pengganti kontinu (*Surrogate Derivative* berupa turunan Fast Sigmoid $\sigma'(x) = \frac{1}{(1 + \beta |x|)^2}$). Latih jaringan SNN untuk klasifikasi sekuensial.
- **Petunjuk Perancangan Arsitektur**:
  - Buat kustom `torch.autograd.Function`: method `.forward()` mengeksekusi operasi biner `(V >= V_th).float()`, method `.backward()` mengeksekusi fungsi surrogate smooth.
  - Simulasikan propagasi temporal melintasi 20 time-step.
  - Terapkan encoding latensi atau rate coding pada input sensorik.
- **Test Vector & Kasus Uji**:
  - Latih pada tugas klasifikasi biner sekuensial sederhana.
  - Gradient check: verifikasi bahwa gradien mengalir lancar dari loss ke parameter bobot sinaptik tanpa mengalami vanishing gradient atau mati nol.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi autograd surrogate gradient presisi, propagasi temporal stabil, konvergensi klasifikasi tercapai.
  - Skor 50%: Model bekerja namun salah mengalikan gradien pada akumulasi langkah waktu temporal.
  - Skor 0%: Menggunakan fungsi autograd standar tanpa surrogate derivative (gradien mati nol total)."""
    },
    198: {
        "trace": r"""#### Tabel Penelusuran Sinyal BCI Implan & Degradasi Dekoding Akibat Gliosis Otak
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Pasca Implan Elektroda Hari 1 | Matriks Array Utah 96 Kanal | Sinyal Local Field Potential (LFP) 1 kHz | Impedansi elektroda optimal: $Z = 250\text{ k}\Omega$ | Sinyal Action Potential tajam (SNR $> 5.0$) | Pasien mengendalikan kursor komputer dengan mulus |
| 2. Kalibrasi Filter Spasial CSP | 96 Sinyal Kanal Mentah | Common Spatial Pattern (CSP) Filter | Matriks kovarians spasial $\Sigma_1$ dan $\Sigma_2$ dihitung | Pembobotan spasial memisahkan niat gerak tangan | Dekoder LDA mencapai akurasi $94.2\%$ |
| 3. Respon Biologis Inflamasi | Jaringan Korteks Motorik Pasien | Proliferasi astrosit & mikroglia di sekitar jarum | Enkapsulasi jaringan parut glia (*Gliosis*) menebal | Impedansi listrik melonjak: $Z \to 2.4\text{ M}\Omega$ | Amplitudo sinyal listrik saraf teredam drastis $-80\%$ |
| 4. Pergeseran Kovarians Non-Stasioner | Sinyal BCI Hari ke-45 | Sinyal saraf terdistorsi oleh lapisan glia | Matriks kovarians bergeser melenceng dari kalibrasi awal | Filter CSP statis menghasilkan proyeksi acak | Akurasi prediksi arah kursor anjlok ke $48.5\%$ |
| 5. Mitigasi Dekoding Adaptif Riemann | Geometri Manifold Riemann | Transformasi Kovarians Spasial ke Simetris Positif Definit (SPD) | Jarak Geodesik Riemann: $\delta_R(\Sigma_1, \Sigma_2)$ | Kalibrasi online tanpa pengawasan (*Unsupervised Tracking*) | Akurasi dekoding motorik BCI pulih dan stabil jangka panjang |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Dekoding Motorik Antarmuka Otak-Komputer (BCI) Akibat Pergeseran Impedansi Jaringan Glia (Gliosis)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Dalam uji klinis antarmuka otak-komputer invasif (*Brain-Computer Interface / BCI*) pada dekade 2000-an dan 2010-an (seperti proyek BrainGate), pasien dengan kelumpuhan tetraplegia yang diimplan susunan elektroda mikro Utah Array di korteks motorik primer awalnya mampu menggerakkan kursor komputer atau lengan robotik dengan tingkat presisi tinggi pada minggu-minggu pertama. Namun secara konsisten setelah 1 hingga 3 bulan, performa dekoder BCI mengalami degradasi drastis hingga sistem tidak dapat digunakan kembali.
- **Akar Masalah Rekayasa Neuroengineering & Non-Stasioneritas Sinyal**: Kegagalan ini berakar pada interaksi biokompatibilitas fisik antara elektroda kaku silikon dengan jaringan lunak otak. Sistem imun saraf memicu reaksi peradangan benda asing (*Foreign Body Response*): sel-sel mikroglia dan astrosit bermigrasi membungkus jarum-jarum elektroda, membentuk lapisan jaringan parut padat bernama **Gliosis**. Lapisan jaringan parut biologis ini menaikkan impedansi listrik antarmuka elektroda hingga sepuluh kali lipat, meredam amplitudo potensial aksi (*spike amplitude attenuation*), dan mendorong badan sel neuron menjauh dari ujung sensor. Akibatnya, filter dekoding spasial statis (seperti Common Spatial Pattern / CSP atau Linear Discriminant Analysis / LDA) yang dikalibrasi pada Hari ke-1 mengalami kegagalan proyeksi total (*Covariate Shift*) karena matriks kovarians sinyal saraf telah bergeser secara fisik.""",
            "snippet": r"""```python
# Analisis Cacat Dekoder BCI: Filter Kovarians Statis vs Geometri Manifold Riemann Adaptif
import numpy as np

# DEKODER BCI CACAT: Mengasumsikan matriks filter spasial konstan selamanya
class StaticCSPDecoder:
    def __init__(self, W_spatial_filter):
        self.W = W_spatial_filter # Matriks filter hari pertama
        
    def decode(self, raw_eeg_signals):
        # Mengalikan sinyal mentah dengan filter lama:
        projected = np.dot(self.W, raw_eeg_signals)
        # KASUS GLIOSIS: Ketika impedansi naik dan kanal sinyal bergeser,
        # proyeksi ini menghasilkan fitur sampah (Noise)!
        return projected

# MITIGASI MODERN: Pelacakan Pergeseran Kovarians Adaptif pada Manifold Riemann
from scipy.linalg import logm, expm

class AdaptiveRiemannianDecoder:
    def __init__(self, n_channels):
        self.reference_mean_cov = np.eye(n_channels)
        self.learning_rate = 0.05
        
    def update_online_covariance(self, current_batch_signals):
        # 1. Hitung matriks kovarians sampel saat ini (Symmetric Positive Definite / SPD)
        current_cov = np.cov(current_batch_signals)
        current_cov += np.eye(len(current_cov)) * 1e-6 # Regularisasi numerik
        
        # 2. Pembaruan geodesik rata-rata Riemann (Frechet Mean Tracking)
        # Menyesuaikan titik acuan geometri terhadap pergeseran lambat gliosis
        diff_matrix = logm(np.linalg.solve(self.reference_mean_cov, current_cov))
        self.reference_mean_cov = np.dot(
            self.reference_mean_cov,
            expm(self.learning_rate * diff_matrix)
        )
        return self.reference_mean_cov # Dekoding tetap stabil melintasi bulan!
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Masalah gliosis mendorong inovasi besar dalam perangkat keras dan algoritma BCI: (1) Transisi ke elektroda fleksibel berbasis polimer ultra-tipis (*Flexible Neural Threads*, seperti yang diadopsi oleh Neuralink) yang meminimalkan respon peradangan jaringan glia karena kelenturan mekanis yang menyerupai modulus elastisitas jaringan otak; (2) Algoritma dekoding berbasis **Riemannian Geometry** yang memetakan matriks kovarians ke manifold manifold simetris definit positif (*SPD Manifold*) yang terbukti invarian terhadap degradasi impedansi linier; (3) Pelatihan kalibrasi adaptif harian tanpa pengawasan (*Unsupervised Daily Re-calibration*) yang berjalan di latar belakang saat pengguna tidur."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis modul pra-pemrosesan sinyal elektrofisiologi otak (EEG/LFP) dalam Python menggunakan SciPy: Bangun filter digital bandpass Butterworth orde-4 (rentang frekuensi gelombang Mu/Beta 8-30 Hz) dan filter notch 50/60 Hz untuk membersihkan interferensi harmonik jala-jala listrik PLN.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan `scipy.signal.butter(4, [8, 30], btype='bandpass', fs=fs)`.
  - Terapkan zero-phase filtering menggunakan `scipy.signal.filtfilt()` untuk mencegah distorsi pergeseran fase waktu sinyal motorik.
  - Hitung Power Spectral Density (PSD) sebelum dan sesudah filtering menggunakan metode Welch (`scipy.signal.welch`).
- **Test Vector & Kasus Uji**:
  - Masukkan sinyal sintetis yang terkontaminasi noise frekuensi 50 Hz beramplitudo tinggi.
  - Pada sinyal hasil filter, puncak spektral pada frekuensi 50 Hz harus diredam minimal sebesar $-40\text{ dB}$, sedangkan komponen 12 Hz dipertahankan utuh.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Filter Butterworth dan Notch presisi, zero-phase filtering diterapkan, visualisasi PSD jelas.
  - Skor 50%: Filter bekerja namun menggunakan pemfilteran satu arah (`lfilter`) yang memicu delay fase waktu sinyal.
  - Skor 0%: Salah menentukan parameter frekuensi cutoff normalisasi Nyquist.

### Tingkat 2: Menengah
- **Tugas**: Bangun algoritma ekstraksi fitur Common Spatial Pattern (CSP) dari nol dalam Python menggunakan dekomposisi nilai eigen simultan (*Joint Diagonalization of Covariance Matrices*) untuk memisahkan dua kelas sinyal Motor Imagery (Gerakan Tangan Kiri vs Tangan Kanan).
- **Petunjuk Perancangan Arsitektur**:
  - Hitung rata-rata matriks kovarians spasial normalisasi $\Sigma_1$ dan $\Sigma_2$ dari setiap kelas.
  - Selesaikan masalah generalized eigenvalue: $\Sigma_1 w = \lambda (\Sigma_1 + \Sigma_2) w$.
  - Pilih $m=2$ filter spasial pertama dan $m=2$ filter spasial terakhir sebagai vektor proyeksi matriks $W_{\text{CSP}}$.
  - Hitung fitur log-variance dari sinyal yang telah diproyeksikan: $f = \log(\text{var}(W_{\text{CSP}} X))$.
- **Test Vector & Kasus Uji**:
  - Uji pada dataset benchmark BCI Competition IV-2a (atau data sintetis 16-kanal 2-kelas).
  - Latih classifier Linear Discriminant Analysis (LDA) di atas fitur log-variance CSP: Akurasi klasifikasi harus mencapai $> 80\%$.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma CSP presisi aljabar linier, ekstraksi fitur log-variance benar, klasifikasi LDA akurat.
  - Skor 50%: CSP bekerja namun lupa melakukan normalisasi jejak (*trace normalization*) pada matriks kovarians.
  - Skor 0%: Menggunakan PCA biasa tanpa memanfaatkan label kelas (unsupervised).

### Tingkat 3: Mahir
- **Tugas**: Rancang modul klasifikasi sinyal saraf berbasis Geometri Manifold Riemann dalam Python: Hitung jarak geodesik affine-invariant (*Affine-Invariant Riemannian Metric / AIRM*) $\delta_R(P_1, P_2) = \|\log(P_1^{-1/2} P_2 P_1^{-1/2})\|_F$ antara dua matriks kovarians spasial, dan bangun algoritma Minimum Distance to Mean (MDM) Classifier yang menghitung Pusat Massa Riemann (*Riemannian Center of Mass / Fréchet Mean*) secara iteratif.
- **Petunjuk Perancangan Arsitektur**:
  - Pastikan seluruh matriks kovarians berstatus Simetris Positif Definit (SPD) via penambahan diagonal kecil (*Tikhonov regularization*).
  - Algoritma Fréchet Mean: Inisialisasi $M = \Sigma_1$, perbarui iteratif pada ruang tangen: $M \leftarrow M^{1/2} \exp\left(\frac{1}{N} \sum \log(M^{-1/2} \Sigma_i M^{-1/2})\right) M^{1/2}$ hingga konvergen.
  - MDM Classifier menetapkan kelas sampel baru ke pusat Riemann kelas terdekat.
- **Test Vector & Kasus Uji**:
  - Bandingkan performa klasifikasi CSP+LDA standar vs Riemannian MDM pada dataset yang mengalami pergeseran derau buatan ($SNR$ turun $-6\text{ dB}$).
  - Riemannian MDM harus mempertahankan akurasi klasifikasi minimal $15\%$ lebih tinggi daripada metode konvensional di bawah degradasi derau.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Implementasi matriks manifold Riemann presisi, konvergensi Fréchet mean akurat, ketahanan terhadap derau terbukti.
  - Skor 50%: Metrik AIRM benar namun menghitung rata-rata kelas menggunakan rata-rata Euclidean biasa (bukan Fréchet mean).
  - Skor 0%: Matriks kovarians tidak dipertahankan sifat simetris positif definitnya (mengalami crash nilai eigen negatif)."""
    },
    199: {
        "trace": r"""#### Tabel Penelusuran Perakitan Genom De Bruijn Graph & Keruntuhan Siklus Elemen Berulang Alu
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Pembacaan Fragmen DNA | Jutaan Pembacaan Pendek (Short Reads 100bp) | Dekomposisi ke k-mer panjang $k=21$ | Penyimpanan k-mer dalam tabel hash memori | Frekuensi k-mer terhitung | Koleksi k-mer mentah siap dipetakan ke graf |
| 2. Konstruksi De Bruijn Graph | Simpul: $(k-1)$-mer, Sisi: $k$-mer | Pembentukan simpul prefix dan suffix | Graf berarah dibangun di memori: $V \to E \to V'$ | Derajat simpul in/out dihitung | Graf merefleksikan tumpang-tindih sekuens genom |
| 3. Pertemuan Elemen Berulang Alu | Sekuens DNA Berulang: 300bp Elemen Alu | Ribuan sekuens identik di berbagai kromosom | Simpul graf bercabang jamak: In-Degree $> 500$, Out-Degree $> 500$ | Ambiguitas topologi graf ekstrem | Jalur Euler kehilangan keunikan deterministik! |
| 4. Keruntuhan Siklus Serakah | Algoritma Assembler Serakah | Pemecahan simpul berulang tanpa petunjuk jarak | Siklus berulang panjang diruntuhkan menjadi 1 simpul tunggal! | Penghapusan sekuens DNA jutaan pasang basa | Genom hasil perakitan terpotong palsu (*Collapsed Assembly*)! |
| 5. Mitigasi Paired-End & Long Reads | Pembacaan Berpasangan (Paired-End) | Penambahan constraint jarak fisik sisipan (*Insert Size*) | Graf diselesaikan menggunakan De Bruijn Berbobot Jalur | Resolusi ambiguitas elemen transposon Alu | Kromosom terakselerasi utuh dengan integritas telomer terjaga |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keruntuhan Perakitan Genom Manusia pada De Bruijn Graph Akibat Elemen Transposon Berulang (Alu Repeats)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Selama perlombaan pengurutan genom Proyek Genom Manusia (*Human Genome Project / Celera Genomics*) pada akhir 1990-an dan era awal Next-Generation Sequencing (NGS) tahun 2008-2012, algoritma perakitan sekuens otomatis berbasis komputer (*De Novo Sequence Assemblers*) berulang kali menghasilkan draf genom manusia yang berlubang, terpotong-potong secara keliru, dan kehilangan puluhan juta pasang basa penting.
- **Akar Masalah Rekayasa Bioinformatika & Teori Graf De Bruijn**: Algoritma perakitan sekuens memecah jutaan pembacaan pendek DNA menjadi sub-string berukuran $k$ (*k-mers*) dan membangun Graf De Bruijn di mana perakitan genom diselesaikan dengan mencari Jalur Euler (*Eulerian Path*). Cacat struktural fatal muncul karena genom manusia tersusun atas lebih dari $50\%$ elemen berulang (*repetitive elements*), khususnya retrotransposon elemen *Alu* (panjang $\approx 300$ pasang basa yang muncul lebih dari 1 juta kali di seluruh kromosom). Jika panjang $k$-mer ($k \approx 31-55$) jauh lebih pendek daripada panjang pengulangan biologis, graf De Bruijn mengalami **Topological Collapse**: ribuan lokus independen dari kromosom yang berbeda terkompresi menjadi satu simpul kusut yang sama di graf. Algoritma perakitan serakah memotong pengulangan tersebut atau menyatukan fragmen dari kromosom yang sama sekali berbeda (*chimeric contigs*), menghilangkan sekuens gen fungsional.""",
            "snippet": r"""```python
# Analisis Topologi De Bruijn Graph: Keruntuhan Siklus Elemen Berulang (Repeat Collapse)
from collections import defaultdict

def build_de_bruijn_graph(reads, k):
    edges = []
    nodes = set()
    for read in reads:
        for i in range(len(read) - k + 1):
            kmer = read[i:i+k]
            prefix = kmer[:-1]
            suffix = kmer[1:]
            nodes.add(prefix)
            nodes.add(suffix)
            edges.append((prefix, suffix))
    return nodes, edges

# KASUS CACAT REPEAT COLLAPSE:
# Sekuens genom asli: "PREFIX_ALUREPEAT_MIDDL1_ALUREPEAT_SUFFIX"
# Dua elemen berulang identik "ALUREPEAT" dengan panjang > k
def demonstrate_repeat_ambiguity():
    # Jika k lebih kecil dari panjang repeat, graf membentuk loop tangensial:
    # Simpul ALU memiliki derajat masuk >= 2 dan derajat keluar >= 2!
    # Akibatnya: Jalur Euler tidak lagi unik!
    # Assembler dapat menyambungkan PREFIX langsung ke SUFFIX,
    # menghilangkan fragmen MIDDL1 sepenuhnya dari genom rakitan!
    return "REPEAT_COLLAPSE_DETECTED"
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Krisis perakitan elemen berulang melahirkan revolusi instrumen bioinformatika modern: (1) Adopsi teknologi sekuensing pembacaan panjang generasi ketiga (**Third-Generation Long Reads: Pacific Biosciences HiFi & Oxford Nanopore**) yang menghasilkan panjang pembacaan $> 20.000$ pasang basa, melompati seluruh elemen berulang Alu secara fisik; (2) Pengembangan algoritma perakitan graf tali (*String Graph & Overlap-Layout-Consensus*) dan **K-mer Size Optimization** dinamis; (3) Keberhasilan perakitan genom manusia lengkap tanpa celah pertama di dunia pada tahun 2022 oleh konsorsium Telomere-to-Telomere (T2T-CHM13)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Implementasikan algoritma perakitan sekuens DNA De Bruijn Graph sederhana dari nol dalam Python: Buat fungsi yang menerima kumpulan potongan sekuens pendek (*reads*), memecahnya menjadi $k$-mer, membangun graf keterhubungan simpul $(k-1)$-mer, dan menemukan Jalur Euler (*Eulerian Path*) menggunakan algoritma Hierholzer untuk merekonstruksi sekuens untai DNA asli.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan graf sebagai adjacency list `defaultdict(list)`.
  - Hitung in-degree dan out-degree setiap simpul untuk menemukan simpul awal (di mana $\text{out} - \text{in} = 1$) dan simpul akhir ($\text{in} - \text{out} = 1$).
  - Gunakan algoritma Hierholzer berbasis tumpukan (*stack*) untuk menelusuri sirkuit Euler dalam waktu linier $\mathcal{O}(|E|)$.
- **Test Vector & Kasus Uji**:
  - Reads: `["TAATGCCATA", "ATGCCATAGC", "CCATAGCATG"]`, $k = 4$.
  - Algoritma harus merekonstruksi sekuens penuh yang benar secara deterministik.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma Hierholzer presisi, rekonstruksi untai DNA utuh, penanganan derajat simpul tepat.
  - Skor 50%: Graf terbangun benar namun penelusuran jalur gagal menangani simpul bercabang.
  - Skor 0%: Menggunakan pencarian permutasi brute force faktorial $\mathcal{O}(N!)$.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul penjajaran sekuens global Needleman-Wunsch (Dynamic Programming Sequence Alignment) dari nol dalam Python: Hitung matriks skor keselarasan antara dua untai DNA/Protein menggunakan model penalti celah linier (*Linear Gap Penalty*) atau affine gap penalty, lalu lakukan traceback untuk menampilkan alignment optimal beserta skor numeriknya.
- **Petunjuk Perancangan Arsitektur**:
  - Skor parameter: Match $= +1$, Mismatch $= -1$, Gap Penalty $= -2$.
  - Matriks DP berukuran $(N+1) \times (M+1)$ dengan inisialisasi baris/kolom nol terakumulasi penalti gap.
  - Rekam pointer arah traceback (Diagonal, Atas, Kiri) untuk merekonstruksi string alignment dengan karakter `'-'` untuk gap.
- **Test Vector & Kasus Uji**:
  - Sekuens 1: `"GATTACA"`, Sekuens 2: `"GCATGCU"`.
  - Algoritma harus menghasilkan alignment optimal dengan skor yang cocok dengan standar BLAST.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Matriks DP dan traceback presisi, visualisasi alignment format BLAST rapi, kompleksitas waktu $\mathcal{O}(NM)$.
  - Skor 50%: Skor matriks benar namun traceback menghasilkan string alignment yang terbalik atau salah menempatkan gap.
  - Skor 0%: Menggunakan pencocokan string greedy biasa tanpa matriks DP.

### Tingkat 3: Mahir
- **Tugas**: Rancang algoritma pencarian pencocokan pola genomik berkecepatan tinggi berbasis Burrows-Wheeler Transform (BWT) dan Ferragina-Manzini Index (FM-Index) dalam Python: Implementasikan transformasi BWT dari string referensi genomik, bangun tabel frekuensi kemunculan karakter (*Occ Table / Rank Table*), dan selesaikan pencarian keberadaan pola sub-string pendek (*Exact Pattern Matching*) dalam waktu proporsional terhadap panjang kueri $\mathcal{O}(P)$ tanpa bergantung pada panjang genom referensi.
- **Petunjuk Perancangan Arsitektur**:
  - Tambahkan sentry karakter `'$'` yang bernilai leksikografis terkecil pada ujung teks.
  - Bangun tabel BWT menggunakan Suffix Array.
  - Implementasikan algoritma Backward Search: Perbarui rentang baris `[top, bottom]` dari karakter terakhir kueri mundur ke depan menggunakan formula $top = C[c] + Occ(c, top - 1) + 1$.
- **Test Vector & Kasus Uji**:
  - Masukkan teks genomik referensi 10.000 pasang basa.
  - Kueri pola: `"ACGTTAGC"` (panjang 8 karakter).
  - Algoritma FM-Index harus menemukan seluruh posisi kemunculan tepat dalam $< 100$ siklus komputasi CPU murni independen dari ukuran genom referensi.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Konstruksi BWT presisi, algoritma Backward Search FM-Index tepat, kompleksitas kueri $\mathcal{O}(P)$ terbukti.
  - Skor 50%: BWT terbangun benar namun pencarian mundur salah memetakan indeks rank pada tabel Occ.
  - Skor 0%: Melakukan pemindaian string linear biasa pada teks asli."""
    },
    200: {
        "trace": r"""#### Tabel Penelusuran Model Mental Kognitif Pilot Air France 447 & Bias Otomasi Sidestick
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Kondisi Jelajah Normal t=0 | Altitudo: 35.000 Kaki, Mach 0.8 | Autopilot Aktif: Normal Law Airbus A330 | Parameter trim horizontal stabil pada $3.0^\circ$ | Beban kognitif pilot rendah (Monitoring Mode) | Penerbangan stabil melintasi Samudra Atlantik |
| 2. Pembekuan Tabung Pitot | Kristal Es Menyumbat Sensor Pitot | Kehilangan Kecepatan Udara (*Unreliable Airspeed*) | Autopilot terputus otomatis! Hukum terbang beralih: *Alternate Law* | Peringatan alarm kokpit berbunyi serentak | Proteksi Flight Envelope otomatis nonaktif! |
| 3. Bias Kognitif Tunneling | Pilot Terbang Terkejut (*Startle Effect*) | Pilot panik menarik sidestick ke belakang penuh (*Nose-Up*) | Model mental keliru: Mengira pesawat overspeed | Kelebihan beban kognitif memblokir penalaran rasional | Hidung pesawat mendongak tajam ke $+16^\circ$ |
| 4. Desain Sidestick Asinkron | Dual Sidestick Pasif Tanpa Gandar Mekanis | Ko-pilot kiri mendorong sidestick ke depan (*Nose-Down*) | Komputer pesawat merata-ratakan kedua input: $Input = \frac{Pos_1 + Pos_2}{2}$ | Ko-pilot kiri tidak sadar rekan kanannya terus menarik stick! | Komando nose-up pilot kanan membatalkan nose-down! |
| 5. Keruntuhan Aerodinamika (Stall) | Sayap Kehilangan Gaya Angkat | Peringatan stall bersuara: *"STALL, STALL!"* diabaikan | Sayap masuk ke dalam *Deep Aerodynamic Stall* penuh | Pesawat jatuh bebas vertikal $10.000\text{ kaki/menit}$ | 228 jiwa melayang di dasar Atlantik akibat kegagalan interaksi manusia-mesin |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Tragedi Jatuhnya Pesawat Air France Penerbangan 447 & Kegagalan Kognitif Antarmuka Sidestick (2009)",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada 1 Juni 2009, pesawat Airbus A330-200 (Air France Penerbangan 447) yang terbang dari Rio de Janeiro menuju Paris jatuh ke Samudra Atlantik di tengah badai tropis, menewaskan seluruh 228 penumpang dan awak pesawat. Investigasi kecelakaan udara oleh BEA Prancis membutuhkan waktu tiga tahun hingga kotak hitam perekam penerbangan berhasil diangkat dari dasar laut kedalaman 4.000 meter.
- **Akar Masalah Rekayasa Faktor Manusia (Human Factors) & Psikologi Kognitif**: Pemicu teknis awal adalah pembekuan sementara kristal es pada tabung sensor kecepatan Pitot (*Pitot probes*). Namun, pesawat sebenarnya dalam kondisi fisik prima. Tragedi fatal terjadi karena kegagalan antarmuka kognitif antara manusia dan sistem otomasi (*Human-Machine Interface / HMI*): (1) **Cognitive Tunneling & Startle Effect**: Ketika autopilot terputus tiba-tiba di tengah turbulensi malam hari, pilot terbang mengalami kelebihan beban sensorik (*cognitive overload*). Alih-alih mempertahankan sikap terbang datar (*pitch and power*), pilot merespons secara panik dengan menarik tongkat kemudi (*sidestick*) ke belakang penuh secara terus-menerus, mendongakkan hidung pesawat hingga terjadi stall aerodinamis; (2) **Cacat Antarmuka Dual-Sidestick Tanpa Umpan Balik Aktif**: Berbeda dengan kontrol yoke tradisional Boeing yang terhubung secara mekanis sehingga kedua pilot dapat melihat dan merasakan pergerakan fisik kemudi satu sama lain, sidestick Airbus A330 tidak memiliki kopling mekanis aktif (*uncoupled passive sidesticks*). Kapten dan ko-pilot kiri tidak dapat melihat bahwa ko-pilot kanan terus-menerus menarik stick ke belakang. Algoritma kontrol pesawat hanya menjumlahkan dan merata-ratakan input dari kedua stick, menyembunyikan input yang saling bertentangan hingga pesawat jatuh bebas ke laut.""",
            "snippet": r"""```python
# Analisis Cacat Antarmuka Sidestick: Perata-rataan Input Tanpa Gandar Mekanis
class UncoupledDualSidestickSystem:
    def __init__(self):
        self.pilot_left_deflection = 0.0   # Rentang [-1.0 (Down) s/d +1.0 (Up)]
        self.pilot_right_deflection = 0.0
        
    # KASUS CACAT DESAIN ASLI AF447:
    # Dua sidestick tidak saling bergerak secara fisik (No Cross-Coupling Force Feedback)
    def calculate_control_surface_command(self):
        # Jika kedua pilot menggerakkan stick secara bersamaan tanpa menekan tombol override:
        # Komputer penerbangan merata-ratakan kedua sinyal input!
        total_command = (self.pilot_left_deflection + self.pilot_right_deflection) / 2.0
        
        # TRAGEDI AF447: Ko-pilot kiri berusaha menukikkan hidung (deflection = -1.0),
        # namun ko-pilot kanan panik menarik hidung (deflection = +1.0)!
        # Hasilnya: command = 0.0 (Netral) atau tetap mendongak jika ko-pilot kanan lebih agresif!
        # Ko-pilot kiri TIDAK MELIHAT atau MERASAKAN bahwa rekannya menarik stick!
        return total_command

# MITIGASI MODERN: Active Inceptor System (Gandar Elektronik Aktif dengan Force Feedback)
class ActiveCrossCoupledSidestick:
    def update_actuators(self, left_input, right_input):
        # Motor servo elektrik secara fisik menggerakkan stick sebelah kiri
        # ketika stick kanan digerakkan, memberikan umpan balik taktil seketika!
        tactile_force_feedback_motor(left_stick_pos=right_input)
        tactile_force_feedback_motor(right_stick_pos=left_input)
        
        if abs(left_input - right_input) > 0.3:
            # Alarm suara vokal instan jika ada dua input bertentangan:
            trigger_cockpit_audio_alert("DUAL_INPUT_DISAGREE")
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Investigasi BEA merevolusi desain rekayasa sistem antarmuka penerbangan dan kognisi: (1) Adopsi teknologi **Active Cross-Coupled Sidesticks** (seperti pada Gulfstream G500 dan pesawat tempur modern) di mana motor servo secara aktif menggerakkan stick pilot lain sehingga terjadi kesadaran situasional bersama (*Shared Situational Awareness*); (2) Desain ulang logika alarm stall kokpit yang tidak boleh mati ketika kecepatan udara turun di bawah batas minimum tertentu; (3) Pelatihan psikologi kognitif **Upset Prevention and Recovery Training (UPRT)** berkala untuk melatih pilot mengatasi bias kognitif panik (*Startle Effect*) di simulator penerbangan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun mesin keadaan berhingga (*Finite State Machine / FSM*) dalam Python yang memodelkan siklus beban kognitif operator manusia (State: *Underload, Optimal, High Load, Cognitive Tunneling/Crash*) berdasarkan laju kejadian stimuli masuk per detik, lengkap dengan transisi penurunan probabilitas keberhasilan keputusan (*Human Error Probability*) mengikuti Hukum Yerkes-Dodson.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan kurva Yerkes-Dodson: Kinerja optimal berada pada tingkat arousal menengah ($A_{\text{opt}}$).
  - Jika laju input stimuli $> \text{Threshold}_{\text{crit}}$ selama $> 5$ detik berturut-turut, transisikan FSM ke status `COGNITIVE_TUNNELING`.
  - Pada status tunneling, filter masukan operator hanya memproses 1 jenis stimuli dan mengabaikan seluruh stimuli periferal lainnya.
- **Test Vector & Kasus Uji**:
  - Simulasi 10 detik dengan laju input normal (2 stimuli/detik): Operator mempertahankan akurasi keputusan $> 95\%$.
  - Simulasi ledakan alarm darurat (20 stimuli/detik): FSM harus beralih ke `COGNITIVE_TUNNELING` dan mengabaikan alarm sekunder.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemodelan FSM Yerkes-Dodson presisi, fenomena tunneling terbukti empiris dalam simulasi.
  - Skor 50%: FSM bekerja namun tingkat galat hanya dimodelkan linier tanpa kurva lonceng Yerkes-Dodson.
  - Skor 0%: Operator selalu merespons seluruh stimuli tanpa batasan beban kognitif.

### Tingkat 2: Menengah
- **Tugas**: Bangun modul antarmuka keselamatan kritis (*Safety Interlock Arbiter*) dalam C/Python yang menerima dua saluran input kontrol manusia independen: Implementasikan deteksi konflik input (*Dual Input Disagree*), mekanisme pembatalan darurat (*Priority Takeover Pushbutton*), dan logika fail-safe yang tidak pernah merata-ratakan input kemudi jika selisihnya melampaui ambang batas berbahaya.
- **Petunjuk Perancangan Arsitektur**:
  - Struktur input: `Channel A (float)`, `Channel B (float)`, `Priority_Button_A (bool)`, `Priority_Button_B (bool)`.
  - Jika selisih $|A - B| > 0.4$ dan tidak ada tombol prioritas yang ditekan: Alihkan kemudi ke status netral aman, bunyikan alarm peringatan audio, dan aktifkan autopilot fallback.
  - Jika salah satu tombol prioritas ditekan selama $> 2$ detik, wewenang dialihkan penuh ke saluran tersebut dan saluran lainnya dinonaktifkan.
- **Test Vector & Kasus Uji**:
  - Masukkan $A = +0.8$ (Nose Up) dan $B = -0.8$ (Nose Down) tanpa tombol prioritas: Arbiter harus menolak perata-rataan input dan memicu alarm `DUAL_INPUT_ALERT`.
  - Pilot A menekan tombol prioritas: Output kemudi seketika mengikuti Saluran A sepenuhnya.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Logika arbitrase input presisi, penanganan takeover tombol prioritas benar, kebal terhadap kompromi perata-rataan naif.
  - Skor 50%: Logika bekerja namun tidak memiliki mekanisme timeout latching pada tombol pengambilalihan wewenang.
  - Skor 0%: Melakukan perata-rataan linier sederhana saat terjadi konflik input.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator beban kerja kognitif berbasis model arsitektur pikiran ACT-R (atau GOMS / Keystroke-Level Model) dalam Python: Simulasikan interaksi operator terhadap dua desain antarmuka dasbor peringatan (Desain A: Hirarkis Menu vs Desain B: Peta Spasial Terpadu), hitung estimasi waktu persepsi (*Perceptual Cycle* $\approx 100\text{ ms}$), waktu kognisi (*Cognitive Cycle* $\approx 50\text{ ms}$), dan waktu motorik (*Motor Cycle* $\approx 70\text{ ms}$), serta buktikan secara kuantitatif penghematan waktu respon darurat pada Desain B.
- **Petunjuk Perancangan Arsitektur**:
  - Implementasikan siklus aturan produksi ACT-R: Pencocokan Pola $\to$ Resolusi Konflik $\to$ Eksekusi Aksi.
  - Hitung waktu latensi respon total: $T_{\text{response}} = T_{\text{perceptual}} + N_{\text{productions}} \cdot T_{\text{cognitive}} + T_{\text{motor}}$.
  - Masukkan faktor degradasi waktu akibat kelelahan mental (*Mental Fatigue Decay*).
- **Test Vector & Kasus Uji**:
  - Jalankan simulasi 50 tugas darurat: Desain B harus memangkas rata-rata waktu intervensi operator minimal $> 40\%$ dibanding Desain A.
  - Buktikan bahwa pada kondisi kelelahan tinggi, Desain A memicu lonjakan probabilitas salah pencet (*Slips & Lapses*) hingga $3\times$ lebih besar daripada Desain B.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Pemodelan arsitektur kognitif ACT-R/GOMS presisi, parameter waktu siklus fisiologis realistis, perbandingan kuantitatif kuat.
  - Skor 50%: Menghitung waktu respon namun hanya menggunakan estimasi acak tanpa memodelkan siklus kognitif modular.
  - Skor 0%: Mengabaikan batasan memori kerja (*Working Memory Capacity*) manusia."""
    },
    201: {
        "trace": r"""#### Tabel Penelusuran Penguraian Tata Bahasa Bebas Konteks (CFG) & Ledakan Kombinatorial
| Langkah Pemrosesan / Token | Representasi Simbolik / Vektor | Mekanisme Atensi / Transisi State | Status Matriks KV-Cache | Probabilitas Distribusi / Logits | Keluaran / Output Linguistik |
|---|---|---|---|---|---|
| 1. Kalimat Masukan Majemuk | Kalimat: *"I saw the astronomer with a telescope"* | Tokenisasi Aliran Kata: $w_1, w_2, \dots, w_7$ | Tumpukan parser rekursif diinisialisasi | Simbol awal tata bahasa: $S \to NP \; VP$ | Parser mulai menurunkan pohon sintaksis |
| 2. Parsing Top-Down Rekursif | Tata Bahasa CFG dengan Frasa Preposisi (PP) | $VP \to VP \; PP$, $NP \to NP \; PP$ | Fungsi rekursif memanggil dirinya sendiri pada tumpukan memori | Evaluasi aturan berulang tanpa memoization | Tumpukan panggilan rekursif mengembang |
| 3. Ambiguitas Penempelan Frasa | Kalimat Bertingkat dengan 5 Frasa Preposisi | Ambiguitas kombinatorial: Bilangan Catalan $C_n = \frac{1}{n+1} \binom{2n}{n}$ | Jumlah kemungkinan pohon sintaksis meledak eksponensial $\mathcal{O}(2^N)$ | Parser mengevaluasi jutaan pohon duplikat | Alokasi stack memory proses mendekati batas sistem |
| 4. Kehabisan Tumpukan Panggilan | Rekursi Mandek pada Aturan Kiri (Left-Recursion) | $A \to A \alpha \mid \beta$ (Rekursi Kiri Langsung) | Pointer instruksi CPU terjebak dalam pemanggilan rekursif tanpa henti | Buffer stack memori sistem operasi meluap | `Fatal Error: StackOverflowError / Segfault`! |
| 5. Mitigasi Algoritma CYK DP | Penguraian Cocke-Younger-Kasami (CYK) | Bentuk Normal Chomsky (CNF) + Tabel Pemrograman Dinamis 2D | Tabel segitiga $T[i, j]$ menyimpan konstituen parsial ($\mathcal{O}(N^3)$) | Seluruh interpretasi ambiguitas terpetakan rapi | Penguraian kalimat selesai dalam milidetik tanpa rekursi |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ledakan Kombinatorial Ambiguitas Parsing CFG & Keruntuhan Mesin Terjemahan Simbolik Awal",
            "chronology": r"""- **Kronologi & Konteks Sejarah**: Pada era awal komputasi linguistik dan penerjemahan mesin berbasis aturan (*Rule-Based Machine Translation / RBMT*) dekade 1970-an hingga 1980-an (seperti proyek terjemahan ALPAC dan sistem SYSTRAN generasi awal), sistem pemrosesan bahasa alami berulang kali gagal memproses dokumen hukum dan teknis yang memuat kalimat-kalimat panjang, sering kali mengalami hang permanen atau kehabisan memori (*Crash/OOM*).
- **Akar Masalah Rekayasa Kompilator Bahasa & Ambiguitas Sintaksis**: Bahasa alami manusia memiliki sifat ambiguitas struktural yang sangat kaya, salah satu yang paling terkenal adalah masalah penempelan frasa preposisi (*Prepositional Phrase Attachment Ambiguity*, misalnya kalimat: *"I saw the man on the hill with a telescope"*). Ketika tata bahasa bebas konteks (*Context-Free Grammar / CFG*) diuraikan menggunakan parser rekursif top-down naif tanpa pemrograman dinamis, jumlah kemungkinan pohon sintaksis bertumbuh mengikuti deret Bilangan Catalan ($C_n$), yang bersifat eksponensial $\mathcal{O}(4^n / n^{3/2})$. Untuk kalimat dengan 10 frasa preposisi bertumpuk, terdapat lebih dari 16.796 variasi pohon parsing yang valid secara tata bahasa. Parser naif mengevaluasi ulang sub-struktur yang sama miliaran kali, menguras tumpukan panggilan (*call stack exhaustion*) dan menghasilkan terjemahan yang sepenuhnya keliru karena tidak memiliki model probabilitas untuk memilih struktur yang paling masuk akal.""",
            "snippet": r"""```python
# Analisis Kerapuhan Parser Rekursif Naif vs Pemrograman Dinamis CYK
# KASUS CACAT: Parser top-down rekursif murni tanpa memoization (Eksponensial O(2^N))
def naive_recursive_parse(tokens, grammar, current_symbol):
    # Jika tata bahasa memuat left-recursion: A -> A alpha
    # Parser langsung terjebak dalam infinite loop stack overflow!
    if not tokens:
        return []
    # Eksplorasi seluruh cabang aturan menghasilkan ledakan kombinatorial:
    valid_trees = []
    # Mengevaluasi ulang frasa konstituen yang sama berulang-ulang tanpa cache!
    return valid_trees

# MITIGASI MODERN: Algoritma Cocke-Younger-Kasami (CYK) Berbasis Dynamic Programming O(N^3)
def cyk_parse_chart(tokens, cnf_grammar):
    '''
    CYK Parser menggunakan tabel DP 2D segitiga untuk menyimpan konstituen yang sudah diuraikan.
    Menghilangkan evaluasi redundan dan membatasi kompleksitas waktu O(N^3 * |G|).
    '''
    n = len(tokens)
    # Inisialisasi chart DP: table[panjang_subkata][indeks_awal] = set(non_terminals)
    table = [[set() for _ in range(n)] for _ in range(n + 1)]
    
    # 1. Basis: Aturan Leksikal Terminal A -> 'word'
    for i, word in enumerate(tokens):
        for lhs, rhs in cnf_grammar.terminal_rules.items():
            if word in rhs:
                table[1][i].add(lhs)
                
    # 2. Langkah Rekursif DP: Menggabungkan sub-frasa (Panjang 2 s/d N)
    for length in range(2, n + 1):
        for start in range(n - length + 1):
            for split in range(1, length):
                left_cell = table[split][start]
                right_cell = table[length - split][start + split]
                
                # Cari aturan biner: A -> B C
                for B in left_cell:
                    for C in right_cell:
                        for lhs in cnf_grammar.binary_rules.get((B, C), []):
                            table[length][start].add(lhs)
                            
    # Jika simbol awal 'S' berada di sel puncak table[n][0], kalimat valid secara tata bahasa!
    is_valid = 'S' in table[n][0]
    return is_valid, table
```""",
            "analysis": r"""- **Analisis Forensik & Rekayasa Modern**: Masalah ledakan parsing mentransformasi linguistik komputasional: (1) Adopsi universal **Probabilistic Context-Free Grammars (PCFG)** yang memberikan bobot probabilitas pada setiap aturan produksi untuk secara otomatis memilih satu pohon parsing paling mungkin via algoritma Viterbi-inside-outside; (2) Penerapan **CYK Parsing & Earley Algorithm** berbasis pemrograman dinamis tabel chart untuk menekan kompleksitas ke batas polinomial $\mathcal{O}(N^3)$; (3) Transisi total industri pemrosesan bahasa alami modern ke model berbasis atensi saraf (Transformer) di mana ketergantungan sintaksis dipelajari secara implisit melalui bobot atensi lunak (*Soft Self-Attention*) tanpa memerlukan penguraian pohon simbolik eksplisit."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Tulis program dalam Python untuk mengonversi aturan tata bahasa bebas konteks (CFG) sederhana menjadi Bentuk Normal Chomsky (*Chomsky Normal Form / CNF*), yang memastikan bahwa seluruh aturan produksi hanya memiliki salah satu dari dua bentuk legal: $A \to B \; C$ (dua non-terminal) atau $A \to a$ (satu terminal).
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan 4 tahap standarisasi CNF: (1) Hapus simbol awal dari sisi kanan (tambahkan $S_0 \to S$); (2) Eliminasi aturan-$\epsilon$ ($A \to \epsilon$); (3) Eliminasi aturan unit ($A \to B$); (4) Pecah aturan panjang menjadi rantai aturan biner.
- **Test Vector & Kasus Uji**:
  - Masukan aturan CFG: $S \to A \; B \; C$, $A \to a$, $B \to b$, $C \to c$.
  - Output CNF harus menghasilkan aturan biner bersih: $S_0 \to A \; X_1$, $X_1 \to B \; C$, tanpa aturan dengan 3 simbol di ruas kanan.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Transformasi CNF presisi, penanganan eliminasi aturan unit dan rantai biner akurat.
  - Skor 50%: Bekerja untuk aturan panjang namun gagal menangani aturan unit rekursif.
  - Skor 0%: Membiarkan aturan campuran (non-terminal + terminal) di sisi kanan.

### Tingkat 2: Menengah
- **Tugas**: Bangun implementasi lengkap algoritma CYK (Cocke-Younger-Kasami) dalam Python yang menerima grammar CNF dan kalimat token, membangun tabel segitiga pemrograman dinamis 2D, memvalidasi apakah kalimat gramatikal, dan merekonstruksi pohon sintaksis konkret (*Syntax Parse Tree*) menggunakan backpointer penelusuran balik.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan pointer referensi pemecahan: `table[length][start][lhs] = (split_index, B, C)`.
  - Tulis fungsi rekursif `build_tree(length, start, symbol)` yang menelusuri pointer untuk menghasilkan struktur nested list representasi pohon: `['S', ['NP', 'I'], ['VP', ['V', 'saw'], ...]]`.
- **Test Vector & Kasus Uji**:
  - Masukkan tata bahasa bahasa Inggris mini dan kalimat: *"she eats fish with a fork"*.
  - Algoritma harus menghasilkan tabel CYK lengkap dan mengekstrak minimal satu pohon sintaksis valid yang diakhiri simbol `S`.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Algoritma CYK presisi $\mathcal{O}(N^3)$, ekstraksi pohon parse bertingkat benar, penanganan ambiguitas jamak rapi.
  - Skor 50%: Validasi tabel CYK benar (mengembalikan True/False) namun gagal merekonstruksi representasi pohon sintaksis.
  - Skor 0%: Salah mengindeks sel pemecahan tabel segitiga.

### Tingkat 3: Mahir
- **Tugas**: Rancang parser Probabilistic CYK (PCYK) dalam Python: Setiap aturan CNF memiliki probabilitas logaritmik $\log P(A \to B \; C)$. Implementasikan algoritma Viterbi di atas tabel chart CYK untuk menemukan satu pohon sintaksis yang memiliki probabilitas tertinggi (*Maximum Likelihood Parse Tree*) secara optimal dan efisien.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan probabilitas ruang log (*Log-Space Probabilities*) $\log P$ untuk mencegah underflow numerik pada kalimat panjang: $\text{Score} = \log P_{\text{rule}} + \text{Score}_{\text{left}} + \text{Score}_{\text{right}}$.
  - Simpan hanya skor probabilitas terbaik per non-terminal pada setiap sel tabel: `best_score[length][start][A] = max(...)`.
- **Test Vector & Kasus Uji**:
  - Masukkan kalimat ambigu klasik: *"astronomers saw stars with telescopes"*.
  - Berikan probabilitas aturan di mana penempelan instrumen pada verba `VP` memiliki prior lebih tinggi daripada nomina `NP`.
  - Parser PCYK harus secara otomatis memilih struktur pohon penempelan verba dan mengabaikan interpretasi penempelan nomina yang tidak logis.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Formulasi PCYK log-space presisi, seleksi pohon Viterbi akurat, penanganan underflow floating-point sempurna.
  - Skor 50%: Algoritma bekerja namun mengalikan probabilitas mentah (rentan underflow float ke nol pada kalimat $> 15$ kata).
  - Skor 0%: Mengembalikan sembarang pohon acak tanpa memperhitungkan bobot probabilitas aturan."""
    }
}
