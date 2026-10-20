"""Encyclopedia Tier 13 Part 1: Topics 196 - 201 (Cognitive Science, Computational Neuroscience, Neuroengineering / BCI, Bioinformatics, Cognitive Psychology, Formal Linguistics)
"""

DATA_TIER_13_PART1 = {
    196: {
        "intuition": r"""Apakah sebuah program komputer yang bisa menjawab pertanyaan cerdas benar-benar "berpikir" dan memiliki kesadaran, atau ia hanya memanipulasi simbol matematika tanpa memahami maknanya sama sekali?

Filsuf John Searle mengajukan sebuah eksperimen pikiran terkenal bernama **Kamar Cina (The Chinese Room Argument)** ([Searle - Minds, Brains, and Programs](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/minds-brains-and-programs/DC644B47A4299C637C89572F1244E10)). Bayangkan seseorang yang tidak mengerti bahasa Mandarin sama sekali terkunci di dalam ruangan dengan sebuah buku panduan aturan tebal. Ketika seseorang memasukkan kertas bertuliskan karakter Mandarin dari celah pintu, orang di dalam kamar hanya mencocokkan bentuk simbol tersebut dengan buku aturan, menyalin simbol jawaban yang ditentukan, lalu mengeluarkannya. Bagi orang di luar, ruangan itu tampak fasih berbahasa Mandarin; namun orang di dalam ruangan tidak mengerti satu kata pun!

Untuk memahami pikiran dan sistem cerdas secara utuh, ilmuwan saraf David Marr merumuskan bahwa kita harus menganalisisnya dari tiga tingkat yang berbeda: **Tingkat Komputasi** (apa tujuannya?), **Tingkat Representasi & Algoritma** (bagaimana representasinya?), dan **Tingkat Implementasi Fisik** (bagaimana perangkat keras/biologisnya mewujudkannya?) ([Marr - Vision: A Computational Investigation](https://mitpress.mit.edu/9780262514620/vision/)).""",
        "theory": r"""Formulasi Formal Sains Kognitif & Tiga Tingkat David Marr:

1. **Tri-Level Hypothesis David Marr (1982)**:
* **Tingkat Komputasi (Computational Level)**: Mendefinisikan sasaran abstrak sistem, mengapa komputasi tersebut dilakukan, dan logika kendala tugas:
$$f: \mathcal{X} \to \mathcal{Y}, \quad \text{Objektif: } \arg\min_y \mathcal{L}(y, f(x))$$
* **Tingkat Algoritma & Representasi (Algorithmic / Representational Level)**: Spesifikasi struktur data input/output dan langkah transformasi matematis (misal: representasi matriks float, algoritma Dynamic Programming, pembaruan gradien).
* **Tingkat Implementasi Fisik (Physical Implementation Level)**: Realisasi fisik perangkat keras di mana algoritma dieksekusi (substrat biologis: potensial aksi ionik neuron natrium-kalium, atau substrat silikon: transistor FinFET, gerbang logika CMOS, register SRAM GPU).

2. **Koneksionisme vs Simbolisme Formal (Fodor & Pylyshyn, 1988)**:
Sistem simbolik beroperasi di atas representasi komposisional terstruktur:
$$\text{Arti}(P \land Q) = \mathcal{I}(P) \times \mathcal{I}(Q)$$
Sedangkan sistem koneksionis (jaringan saraf tiruan) merepresentasikan konsep sebagai vektor terdistribusi kontinu dalam ruang manifold $\mathbb{R}^d$, di mana makna semantik muncul dari kedekatan sudut kosinus dot-product ([Fodor & Pylyshyn - Connectionism and Cognitive Architecture](https://www.sciencedirect.com/science/article/pii/0010027788900315)).

3. **Prinsip Energi Bebas Karl Friston (Free Energy Principle)**:
Otak beroperasi sebagai mesin inferensi aktif Bayesian yang berusaha meminimalkan energi bebas variasional $F$ (batas atas dari kejutan persepsi / *surprisal*):
$$F = \mathbb{E}_{q(\vartheta)}[\ln q(\vartheta) - \ln p(\tilde{y}, \vartheta)] = D_{KL}(q(\vartheta) \parallel p(\vartheta \mid \tilde{y})) - \ln p(\tilde{y})$$
Di mana $\tilde{y}$ adalah input sensori dan $\vartheta$ status laten dunia luar ([Friston - The Free-Energy Principle: A Unified Brain Theory?](https://www.nature.com/articles/nrn2787)).""",
        "internals": r"""Struktur dekomposisi hierarki kognitif tiga lapis David Marr yang diaplikasikan pada visi dan AI:

```mermaid
flowchart TD
    subgraph Level_1["1. Tingkat Komputasi (Goals & Theory)"]
        Goal["Tujuan: Menentukan Posisi & Bentuk Objek 3D dari Citra 2D"]
        Constraint["Kendala Fisik: Reflektansi Cahaya, Hukum Optik Geometris"]
    end
    subgraph Level_2["2. Tingkat Representasi & Algoritma"]
        Rep["Representasi: Depth Map, Feature Vectors, Surface Normals"]
        Algo["Algoritma: Konvolusi Spasial, Stereo Matching, Atensi Multi-Head"]
    end
    subgraph Level_3["3. Tingkat Implementasi Fisik"]
        HardwareBio["Biologis: Kolom Korteks V1-V4, Sinapsis Neurotransmiter"]
        HardwareSilicon["Silikon: GPU Tensor Cores, Instruksi SIMD AVX-512, RAM"]
    end
    Level_1 --> Level_2 --> Level_3
```

Kekuatan metodologi Marr adalah *independensi substrat*: algoritma komputasi yang identik dapat dijalankan di jaringan saraf otak manusia berbasis glukosa dan ion, maupun pada kluster superkomputer silikon berdaya listrik tinggi ([David Marr Vision](https://mitpress.mit.edu/9780262514620/vision/)).""",
        "code_block": r"""```python
import numpy as np

# Simulasi Inferensi Prediktif Karl Friston Sederhana (Predictive Coding 1D)
class PredictiveCodingNeuron:
    def __init__(self, prior_mu=0.0, prior_var=1.0, sensory_var=0.2):
        self.mu = prior_mu         # Prediksi internal otak (state representation)
        self.sigma_p = prior_var   # Ketidakpastian prior
        self.sigma_s = sensory_var # Ketidakpastian sensoris
        
    def step(self, sensory_input, lr=0.1):
        # 1. Hitung Prediction Error (Selisih Input Riil vs Ekspektasi)
        prediction_error = sensory_input - self.mu
        
        # 2. Turunan Energi Bebas Variasional terhadap Status Representasi Internal
        # dF/dmu = (mu - prior) / sigma_p - (sensory - mu) / sigma_s
        grad_f = (self.mu - 0.0) / self.sigma_p - (prediction_error) / self.sigma_s
        
        # 3. Pembaruan Status Kognitif untuk Meminimalkan Surprise
        self.mu = self.mu - lr * grad_f
        free_energy = 0.5 * (prediction_error**2 / self.sigma_s) + 0.5 * (self.mu**2 / self.sigma_p)
        return self.mu, prediction_error, free_energy

# Uji Coba: Stimulus Sensoris Tiba-tiba Bernilai 5.0
brain_unit = PredictiveCodingNeuron(prior_mu=0.0)
print("Simulasi Penyesuaian Keyakinan Otak (Minimisasi Free Energy):")
for t in range(1, 11):
    internal_belief, error, f_val = brain_unit.step(sensory_input=5.0, lr=0.05)
    print(f"Langkah {t:02d} | Keyakinan Internal: {internal_belief:.3f} | Pred Error: {error:.3f} | Free Energy: {f_val:.3f}")

assert abs(internal_belief - 4.16) < 0.2, "Model kognitif harus konvergen ke estimasi posterior Bayes!"
```""",
        "pitfalls": r"""*Kekeliruan Homunculus (Homunculus Fallacy)*: Menjelaskan proses berpikir otak dengan mengasumsikan ada "manusia kecil" di dalam kepala yang melihat citra visual dari mata dan membuat keputusan. Hal ini hanya memindahkan masalah tanpa menjelaskannya. Dalam sains kognitif modern, kecerdasan harus diuraikan sebagai fenomena kemunculan (*emergence*) dari miliaran interaksi lokal antar unit sederhana tanpa adanya komandan pusat ([Dennett - Consciousness Explained](https://www.hachettebookgroup.com/titles/daniel-c-dennett/consciousness-explained/9780316217767/)).""",
        "exercises": r"""### Level 1 (Pemula)
Pilih salah satu sistem AI modern (misal: Pengenalan Wajah Smartphone) dan uraikan secara mendalam ke dalam Tiga Tingkat Analisis David Marr (Komputasi, Representasi & Algoritma, dan Implementasi Fisik) dalam format esai terstruktur 1 halaman.
*Rubrik*: Pemisahan yang jelas dan tepat tanpa ada percampuran antar tingkat.

### Level 2 (Menengah)
Bangun simulasi agen pengambil keputusan berbasis *Predictive Processing* di Python: agen memiliki model dunia internal (prediksi posisi makanan), menerima input sensoris berderau, menghitung prediction error spasial 2D, dan menggerakkan aktuatornya untuk mengurangi selisih error tersebut.
*Rubrik*: Agen bergerak secara stabil menuju sumber stimulus tanpa osilasi liar.

### Level 3 (Mahir)
Implementasikan eksperimen komputasional perbandingan representasi simbolik murni (Production Rule System berbasis pohon logika) vs representasi terdistribusi (Word2Vec / neural embedding) dalam menyelesaikan analogi semantik ($A : B = C : ?$). Evaluasi ketahanan terhadap representasi yang tidak lengkap atau ambigu.
*Rubrik*: Analisis kuantitatif kegagalan sistem simbolik terhadap sinonim non-terdaftar.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Vision: A Computational Investigation into the Human Representation | David Marr (MIT AI Lab) | [MIT Press Classic](https://mitpress.mit.edu/9780262514620/vision/) | Fondasi Tiga Tingkat Analisis Kognitif (Marr's Tri-Level) |
| Minds, Brains, and Programs | John R. Searle | [Behavioral and Brain Sciences](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/minds-brains-and-programs/DC644B47A4299C637C89572F1244E10) | Makalah Argumen Kamar Cina (Chinese Room Argument) |
| The Free-Energy Principle: A Unified Brain Theory? | Karl Friston (University College London) | [Nature Reviews Neuroscience](https://www.nature.com/articles/nrn2787) | Kerangka Kerja Prediktif Otak Bayesian & Minimisasi Energi Bebas |
| Connectionism and Cognitive Architecture: A Critical Analysis | Jerry A. Fodor & Zenon W. Pylyshyn | [Cognition Journal](https://www.sciencedirect.com/science/article/pii/0010027788900315) | Debat Filosofis Simbolik Klasik vs Jaringan Syaraf Tiruan |"""
    },
    197: {
        "intuition": r"""Jika Anda memperbesar sepotong jaringan otak di bawah mikroskop elektron, Anda tidak akan melihat kabel tembaga atau transistor silikon. Anda akan melihat 86 miliar sel hidup yang disebut **Neuron**, masing-masing terhubung ke ribuan neuron lain melalui jembatan mikroskopis bernama **Sinapsis** ([Kandel et al. - Principles of Neural Science](https://accessneurology.mhmedical.com/book.aspx?bookid=1049)).

Sebuah neuron tidak bekerja seperti chip komputer digital yang menghitung angka pecahan biner. Neuron bekerja seperti bendungan air bertenaga listrik kimia! Membran neuron memompa ion natrium ($Na^+$) dan kalium ($K^+$) untuk menahan tegangan listrik sekitar $-70\text{ mV}$. Ketika stimulus yang masuk cukup kuat melewati ambang batas tertentu, pintu gerbang bendungan terbuka seketika: tegangan melonjak drastis hingga $+30\text{ mV}$ dalam waktu satu milidetik sebelum turun kembali: ledakan pulsa listrik ini disebut **Potensial Aksi (Spike)**!

Bagaimana kita mengingat sesuatu? Donald Hebb merumuskan aturan emas: *"Neuron that fire together, wire together"* ([Hebb - The Organization of Behavior](https://monoskop.org/images/8/87/Hebb_Donald_O_The_Organization_of_Behavior.pdf)). Jika dua neuron berulang kali melepaskan pulsa listrik pada saat yang hampir bersamaan, hubungan sinapsis di antara mereka akan menebal dan menguat (**Plastisitas Sinaptik / STDP**).""",
        "theory": r"""Formulasi Matematis Biofisika Saraf:

1. **Model Konduktansi Hodgkin-Huxley (1952)**:
Memodelkan membran lipid sel saraf sebagai sirkuit listrik kapasitor paralel dengan saluran konduktansi ionik non-linier ([Hodgkin & Huxley - J. Physiol. 1952](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/)):
$$C_m \frac{dV}{dt} = I_{\text{inj}} - \bar{g}_{Na} m^3 h (V - E_{Na}) - \bar{g}_K n^4 (V - E_K) - \bar{g}_L (V - E_L)$$
Variabel gating $x \in \{m, n, h\}$ berevolusi menurut kinetika Markov orde-1:
$$\frac{dx}{dt} = \alpha_x(V)(1 - x) - \beta_x(V)x = \frac{x_\infty(V) - x}{\tau_x(V)}$$

2. **Model Leaky Integrate-and-Fire (LIF)**:
Aproksimasi analitik sederhana neuron komputasional:
$$\tau_m \frac{dV}{dt} = -(V(t) - V_{\text{rest}}) + R_m I(t)$$
Kondisi Ambang Batas & Reset Refrakter:
$$\text{Jika } V(t) \ge V_{\text{th}} \implies \text{Pancarkan Spike } S(t) = 1, \quad V(t^+) \leftarrow V_{\text{reset}}$$

3. **Plastisitas Bergantung Waktu Pulsa (Spike-Timing-Dependent Plasticity / STDP)**:
Perubahan efikasi bobot sinapsis $\Delta w$ bergantung pada selisih waktu relatif $\Delta t = t_{\text{post}} - t_{\text{pre}}$ antara firing neuron pasca-sinapsis dan pra-sinapsis ([Bi & Poo - Synaptic Modifications in Cultured Hippocampal Neurons](https://www.jneurosci.org/content/18/24/10464)):
$$\Delta w = \begin{cases} A_+ \exp\left(-\frac{\Delta t}{\tau_+}\right), & \text{jika } \Delta t > 0 \quad (\text{LTP - Long-Term Potentiation}) \\ -A_- \exp\left(\frac{\Delta t}{\tau_-}\right), & \text{jika } \Delta t < 0 \quad (\text{LTD - Long-Term Depression}) \end{cases}$$""",
        "internals": r"""Arsitektur rangkaian ekuivalen membran sel Hodgkin-Huxley dan kurva plastisitas sinaptik STDP:

```mermaid
flowchart TD
    subgraph Membrane_Circuit["Sirkuit Biofisika Membran Neuron"]
        Cm["Kapasitansi Membran C_m (1 uF/cm^2)"]
        Na_Ch["Saluran Natrium g_Na * m^3 * h (E_Na = +50 mV)"]
        K_Ch["Saluran Kalium g_K * n^4 (E_K = -77 mV)"]
        Leak["Saluran Kebocoran g_L (E_L = -54 mV)"]
        Cm --- Na_Ch --- K_Ch --- Leak
    end
    subgraph STDP_Mechanism["Aturan Pembelajaran STDP"]
        LTP["t_post > t_pre : Sinapsis Diperkuat (+Delta w)"]
        LTD["t_post < t_pre : Sinapsis Dilemahkan (-Delta w)"]
    end
```

Kunci utama Spiking Neural Networks (SNN) adalah *efisiensi energi komputasi berbasis kejadian (event-driven)*: sinapsis hanya mengonsumsi daya saat terjadi pulsa spike diskret, berbeda dengan deep learning konvensional yang terus-menerus mengalikan matriks floating-point secara masif ([Gerstner & Kistler - Spiking Neuron Models](https://www.cambridge.org/core/books/spiking-neuron-models/0932224A69EBBCA726C78F72AC6AEE89)).""",
        "code_block": r"""```python
import numpy as np

# 1. Simulasi Numerik Neuron Leaky Integrate-and-Fire (LIF)
class LIFNeuron:
    def __init__(self, tau_m=20.0, v_rest=-70.0, v_reset=-75.0, v_th=-50.0, r_m=10.0):
        self.tau_m = tau_m     # Konstanta waktu membran (ms)
        self.v_rest = v_rest   # Potensial istirahat (mV)
        self.v_reset = v_reset # Potensial pasca-spike (mV)
        self.v_th = v_th       # Ambang batas aksi potensial (mV)
        self.r_m = r_m         # Resistansi membran (MOhm)
        self.v = v_rest
        
    def step(self, i_inj, dt=0.1):
        # Persamaan Diferensial Euler: dV/dt = (-(V - V_rest) + R*I) / tau
        dv = (-(self.v - self.v_rest) + self.r_m * i_inj) * (dt / self.tau_m)
        self.v += dv
        
        spiked = False
        if self.v >= self.v_th:
            spiked = True
            self.v = self.v_reset
            
        return self.v, spiked

# Simulasi Respons Terhadap Injeksi Arus Konstan (I = 2.5 nA)
neuron = LIFNeuron()
spike_times = []
dt = 0.1
time_steps = np.arange(0, 100, dt)

for t in time_steps:
    v, spiked = neuron.step(i_inj=2.5, dt=dt)
    if spiked:
        spike_times.append(t)

print(f"Total Potensial Aksi (Spike) Dipancarkan: {len(spike_times)} kali dalam 100 ms")
print(f"Frekuensi Firing Neuron: {len(spike_times) / 0.1:.1f} Hz")
print(f"Spike Pertama Terjadi pada: t = {spike_times[0]:.1f} ms")
```""",
        "pitfalls": r"""*Non-Diferensiabilitas Pulsa Spike (The Gradient Problem in SNN)*: Fungsi output neuron biologis adalah fungsi tangga Heaviside $\Theta(V - V_{th})$ yang memiliki turunan nol di hampir semua titik dan tak hingga saat threshold, membuat algoritma standar backpropagation runtuh seketika. Solusi modern: gunakan teknik **Surrogate Gradient** (mengganti turunan Heaviside dengan turunan fungsi kontinu halus seperti fast sigmoid atau arctan selama backward pass) ([Neftci et al. - Surrogate Gradient Learning in Spiking Neural Networks](https://arxiv.org/abs/1901.09948)).""",
        "exercises": r"""### Level 1 (Pemula)
Simulasikan neuron Leaky Integrate-and-Fire (LIF) dengan berbagai variasi arus injeksi $I_{\text{inj}} \in [0.5, 5.0]\text{ nA}$, buat kurva relasi arus terhadap frekuensi firing (Kurva $f$-$I$), dan tentukan arus threshold minimum $I_{\text{rheobase}}$.
*Rubrik*: Grafik kurva f-I menunjukkan karakteristik disipasi threshold yang tepat.

### Level 2 (Menengah)
Implementasikan simulasi persamaan biofisika Hodgkin-Huxley 4-variabel $(V, m, n, h)$ menggunakan integrasi numerik Runge-Kutta orde-4 (RK4) di Python. Tampilkan bentuk gelombang potensial aksi lengkap mencakup fase depolarisasi, repolarisasi, dan refrakter hiperpolarisasi.
*Rubrik*: Menghasilkan lonjakan voltase hingga $+30\text{ mV}$ dengan durasi pulsa $\approx 2\text{ ms}$.

### Level 3 (Mahir)
Bangun simulasi Spiking Neural Network (SNN) 2-lapisan dengan aturan plastisitas sinaptik STDP online murni tanpa pengawasan: latih jaringan untuk mengelompokkan dua pola input pulsa temporal yang berbeda dan buktikan konvergensi bobot sinaptik ke representasi selektif.
*Rubrik*: Terjadi pemisahan bobot sinaptik bimodal (pembagian kelompok bobot kuat dan lemah).""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| A Quantitative Description of Membrane Current (Hodgkin-Huxley) | A. L. Hodgkin & A. F. Huxley | [Journal of Physiology 1952 Classic](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1392413/) | Persamaan Asli Biofisika Potensial Aksi Ionik |
| Principles of Neural Science (5th Ed.) | Eric R. Kandel et al. (Nobel Laureate) | [AccessNeurology McGraw-Hill](https://accessneurology.mhmedical.com/book.aspx?bookid=1049) | Alkitab Neurosains: Biofisika, Kanal Ionik, Sinapsis |
| Synaptic Modifications in Cultured Hippocampal Neurons (STDP) | Guo-qiang Bi & Mu-ming Poo | [Journal of Neuroscience 1998](https://www.jneurosci.org/content/18/24/10464) | Bukti Eksperimental Asli Kurva Waktu Plastisitas STDP |
| Spiking Neuron Models: Single Neurons, Populations, Plasticity | Wulfram Gerstner & Werner M. Kistler | [Cambridge University Press](https://www.cambridge.org/core/books/spiking-neuron-models/0932224A69EBBCA726C78F72AC6AEE89) | Matematika Pemodelan LIF, SRM, dan Dinamika Jaringan Spiking |"""
    },
    198: {
        "intuition": r"""Bayangkan Anda lumpuh total karena cedera saraf tulang belakang, tidak bisa menggerakkan tangan atau berbicara, tetapi pikiran sadar Anda di dalam otak tetap bekerja 100% normal. Bagaimana jika sebuah komputer bisa membaca niat di dalam pikiran Anda dan menggerakkan lengan robot atau mengetik kata-kata di layar monitor secara langsung?

Itulah misi **Antarmuka Otak-Komputer (Brain-Computer Interface / BCI)** ([Wolpaw et al. - Brain-Computer Interfaces for Communication and Control](https://www.sciencedirect.com/science/article/pii/S1388245702000573)). Ketika Anda berniat menggerakkan tangan kanan Anda, jutaan neuron di korteks motorik otak Anda menyala serempak, memancarkan gelombang osilasi listrik mikro.

Sensor dapat dipasang di luar kulit kepala tanpa operasi (**EEG / Elektroensefalografi**), diletakkan langsung di permukaan jaringan otak (**ECoG / Elektrokortikografi**), atau ditanam ke dalam neuron via benang elektroda mikro (seperti implan Neuralink). Sinyal listrik biologis berukuran mikrovolt ($10^{-6}\text{ V}$) yang penuh derau ini disaring, diekstraksi menggunakan matematika filter spasial (*Common Spatial Patterns*), lalu diterjemahkan oleh algoritma decoding menjadi perintah kendali fisik ([Rao - Brain-Computer Interfacing: An Introduction](https://www.cambridge.org/core/books/braincomputer-interfacing/9780521769419)).""",
        "theory": r"""Formulasi Matematis Akuisisi & Pemrosesan Sinyal Neuroengineering:

1. **Model Elektrodinamika Dipol Sumber EEG**:
Potensial listrik $V(r)$ pada elektroda permukaan kulit kepala merupakan superposisi linier arus pasca-sinaptik dari jutaan sel piramidal kortikal yang berorientasi paralel:
$$V(r) = \frac{1}{4\pi \sigma} \int \frac{\nabla \cdot J_{\text{imprecised}}(r')}{\|r - r'\|} dr'$$
Di mana $\sigma$ adalah konduktivitas jaringan berlapis (otak, cairan serebrospinal, tengkorak, kulit kepala).

2. **Common Spatial Pattern (CSP) Filtering**:
Mencari filter spasial $w \in \mathbb{R}^C$ yang memaksimalkan varians sinyal untuk satu kelas motor imagery (misal bayangan gerak tangan kanan) sekaligus meminimalkan varians untuk kelas lain (tangan kiri) ([Blankertz et al. - Optimizing Spatial filters for Robust EEG BCI](https://ieeexplore.ieee.org/document/4408441)):
$$\arg\max_w \frac{w^T \Sigma_1 w}{w^T \Sigma_2 w} \quad \text{ekuivalen dengan masalah General Eigenvalue: } \Sigma_1 w = \lambda \Sigma_2 w$$
Di mana $\Sigma_1$ dan $\Sigma_2$ adalah matriks kovarians rata-rata sinyal EEG multi-kanal pada kedua kondisi.

3. **Irama Gelombang Otak & Sensorimotor Rhythms (SMR)**:
* Gelombang Delta ($\delta$): $0.5 - 4\text{ Hz}$ (Tidur lelap non-REM)
* Gelombang Theta ($\theta$): $4 - 8\text{ Hz}$ (Mengantuk, meditasi dalam)
* Gelombang Alpha ($\alpha$ / Irama $\mu$ Motorik): $8 - 12\text{ Hz}$ (Relaksasi mata tertutup; tersupresi saat niat bergerak / *Event-Related Desynchronization (ERD)*)
* Gelombang Beta ($\beta$): $13 - 30\text{ Hz}$ (Konsentrasi aktif, pemulihan motorik)
* Gelombang Gamma ($\gamma$): $> 30\text{ Hz}$ (Integrasi informasi kognitif tinggi).""",
        "internals": r"""Arsitektur pipeline pemrosesan sinyal BCI closed-loop dari korteks ke aktuator:

```mermaid
flowchart LR
    Brain["Aktivitas Saraf Otak (Korteks Motorik)"] --> Electrodes["Elektroda EEG 64-Kanal"]
    Electrodes --> AFE["Analog Front-End (Penguat Bio-Instrumentasi & Notch 50/60Hz)"]
    AFE --> ADC["ADC 24-bit (Sampling 500-1000 Hz)"]
    ADC --> Bandpass["Bandpass Filter (8-30 Hz Mu/Beta Rhythm)"]
    Bandpass --> CSP["Common Spatial Pattern (CSP Spatial Projection)"]
    CSP --> Classifier["Klasifikasi Machine Learning (LDA / SVM)"]
    Classifier --> Actuator["Aktuator Robotik / Kursor Virtual"]
    Actuator -.->|"Umpan Balik Visual (Visual Feedback)"| Brain
```

Tantangan utama sistem non-invasif adalah *Skull Attenuation*: tulang tengkorak manusia bertindak sebagai filter low-pass kapasitif yang meredam sinyal berfrekuensi tinggi ($>40\text{ Hz}$) dan menyebarkan sinyal spasial secara difus (*volume conduction effect*), menuntut filtering spasial canggih ([Nunez & Srinivasan - Electric Fields of the Brain](https://academic.oup.com/book/26815)).""",
        "code_block": r"""```python
import numpy as np
from scipy import signal
from scipy.linalg import eigh

# 1. Implementasi Common Spatial Pattern (CSP) untuk EEG BCI 2-Kelas
class CommonSpatialPattern:
    def __init__(self, n_components=4):
        self.n_components = n_components
        self.filters_ = None
        
    def fit(self, X1, X2):
        # X: array (n_trials, n_channels, n_times)
        def cov_mean(X):
            covs = [np.cov(trial) for trial in X]
            return np.mean(covs, axis=0)
            
        sigma1 = cov_mean(X1)
        sigma2 = cov_mean(X2)
        
        # Generalized Eigenvalue Problem: Sigma1 * w = lambda * (Sigma1 + Sigma2) * w
        vals, vecs = eigh(sigma1, sigma1 + sigma2)
        
        # Urutkan vektor eigen: komponen awal memaksimalkan kelas 1, akhir memaksimalkan kelas 2
        ix = np.argsort(vals)
        vecs = vecs[:, ix]
        half = self.n_components // 2
        self.filters_ = np.hstack([vecs[:, :half], vecs[:, -half:]]).T
        return self
        
    def transform(self, X):
        features = []
        for trial in X:
            # Proyeksi spasial: Z = W * X
            z = np.dot(self.filters_, trial)
            var = np.var(z, axis=1)
            # Log-variance feature extraction
            feat = np.log(var / np.sum(var))
            features.append(feat)
        return np.array(features)

# Simulasi Sinyal EEG Sintetis (8 Kanal, 200 Titik Waktu per Trial, 20 Trial)
np.random.seed(42)
X_left = np.random.randn(20, 8, 200)   # Tangan Kiri
X_right = np.random.randn(20, 8, 200)  # Tangan Kanan
# Tambahkan osilasi ritme mu 10Hz pada kanal 0 untuk tangan kiri
t = np.linspace(0, 1, 200)
X_left[:, 0, :] += 2.0 * np.sin(2 * np.pi * 10 * t)

csp = CommonSpatialPattern(n_components=2)
csp.fit(X_left, X_right)
features_left = csp.transform(X_left)
print(f"Bentuk Matriks Fitur CSP: {features_left.shape} (20 trials x 2 spatial features)")
print(f"Fitur Rata-rata Kelas 1: {np.mean(features_left, axis=0)}")
```""",
        "pitfalls": r"""*Artefak Okular dan Sinyal Otot (EOG & EMG Contamination)*: Kedipan mata (Electrooculography) memancarkan tegangan hingga $1000\mu\text{V}$ (ratusan kali lebih besar dari sinyal EEG asli yang hanya $10-50\mu\text{V}$), sementara ketegangan otot rahang memancarkan sinyal EMG frekuensi tinggi yang menenggelamkan pita gamma. Jika classifier dilatih tanpa pembersihan artefak (*Independent Component Analysis / ICA*), model Anda mungkin hanya mengklasifikasikan kedipan mata atau kertakan gigi alih-alih niat kognitif otak ([Urigüen & Garcia-Zapirain - EEG Artifact Removal Techniques](https://www.sciencedirect.com/science/article/pii/S1053811915000554)).""",
        "exercises": r"""### Level 1 (Pemula)
Rancang filter digital Butterworth Bandpass orde-4 di Scipy untuk menyaring pita frekuensi ritme motorik Alpha/Mu ($8 - 12\text{ Hz}$) pada rekaman sinyal EEG tiruan, dan tampilkan estimasi densitas spektrum daya (*Power Spectral Density - PSD*) menggunakan metode Welch.
*Rubrik*: Grafik PSD menunjukkan pelemahan daya yang tajam di luar pita $8-12\text{ Hz}$.

### Level 2 (Menengah)
Bangun pipeline klasifikasi Motor Imagery lengkap menggunakan dataset publik BCI Competition IV (atau sinyal sintetis 16-kanal): terapkan bandpass filter, ekstraksi fitur Common Spatial Pattern (CSP), latih model Linear Discriminant Analysis (LDA), dan ukur skor akurasi klasifikasi 2-arah.
*Rubrik*: Akurasi klasifikasi mencapai $> 80\%$ pada data pengujian.

### Level 3 (Mahir)
Implementasikan sistem deteksi potensial P300 Speller real-time: proses epoch sinyal EEG pasca-stimulus flash ($0 - 600\text{ ms}$), deteksi puncak gelombang defleksi positif pada interval $300\text{ ms}$, terapkan ensemble averaging untuk menekan noise background, dan petakan ke koordinat matriks huruf $6 \times 6$.
*Rubrik*: Mampu mengeja kata target 5 huruf secara otomatis dari matriks flash stimulasi.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Brain-Computer Interfaces for Communication and Control | Jonathan R. Wolpaw et al. | [Clinical Neurophysiology Review](https://www.sciencedirect.com/science/article/pii/S1388245702000573) | Fondasi Medis BCI, SMR, P300, Slow Cortical Potentials |
| Optimizing Spatial filters for Robust EEG Single-Trial Analysis (CSP) | Benjamin Blankertz et al. | [IEEE Signal Processing Magazine](https://ieeexplore.ieee.org/document/4408441) | Formulasi Matematika Filter Spasial CSP & Regularisasi |
| Electric Fields of the Brain: The Neurophysics of EEG | Paul L. Nunez & Ramesh Srinivasan | [Oxford University Press](https://academic.oup.com/book/26815) | Fisika Medan Elektromagnetik Tengkorak, Model Konduksi Volume |
| An Integrated Brain-Machine Interface Platform with Thousands of Channels | Elon Musk & Neuralink Team | [Journal of Medical Internet Research](https://www.jmir.org/2019/10/e16194/) | Desain Implan Elektroda Fleksibel Berdensitas Tinggi & ASIC |"""
    },
    199: {
        "intuition": r"""Tubuh setiap makhluk hidup di bumi dikendalikan oleh kode perangkat lunak biologis yang ditulis dalam bentuk molekul asam deoksiribonukleat (**DNA**). DNA tersusun dari 4 huruf alfabet kimia sederhana: **A** (Adenin), **C** (Sitosin), **G** (Guanin), dan **T** (Timin) ([Watson & Crick - Nature 1953](https://www.nature.com/articles/171737a0)).

Genom manusia memiliki 3 miliar huruf DNA. Jika kita ingin menemukan apakah seorang pasien memiliki mutasi virus baru atau mutasi kanker tertentu, bagaimana kita mencari kecocokan urutan huruf di antara miliaran kode tersebut tanpa tersesat oleh mutasi acak?

Itulah ranah **Bioinformatika**: perpaduan antara ilmu biologi molekuler, struktur data string tingkat tinggi, dan kecerdasan buatan. Dari algoritma penyejajaran sekuens dinamis klasik (**Smith-Waterman & BLAST**) yang mencocokkan huruf DNA seperti fitur diff pada git, hingga terobosan revolusioner **AlphaFold** yang berhasil memecahkan teka-teki 50 tahun tentang bagaimana rantai kode protein melipat dirinya menjadi struktur fisik 3D berpresisi tingkat atom ([Jumper et al. - Highly Accurate Protein Structure Prediction with AlphaFold](https://www.nature.com/articles/s41586-021-03819-2)).""",
        "theory": r"""Formulasi Matematis Penyejajaran Sekuens & Pemodelan Protein:

1. **Algoritma Penyejajaran Lokal Smith-Waterman**:
Memaksimalkan skor kemiripan lokal antara sekuens $A$ panjang $n$ dan sekuens $B$ panjang $m$ via pemrograman dinamis ([Smith & Waterman - J. Mol. Biol. 1981](https://www.sciencedirect.com/science/article/pii/0022283681900875)):
$$H(i, j) = \max \begin{cases} 0 \\ H(i-1, j-1) + s(A_i, B_j) & \text{(Match / Mismatch)} \\ H(i-1, j) - W_g & \text{(Deletion / Gap di B)} \\ H(i, j-1) - W_g & \text{(Insertion / Gap di A)} \end{cases}$$
Di mana $s(a, b)$ adalah matriks substitusi asam amino (seperti BLOSUM62 atau PAM250), dan penelusuran balik (*backtracking*) dimulai dari nilai maksimum global $\max_{i, j} H(i, j)$ hingga mencapai sel bernilai 0.

2. **Heuristik BLAST (Basic Local Alignment Search Tool)**:
Mempercepat pencarian database genomik dari $\mathcal{O}(NM)$ menjadi sub-linier melalui pencocokan kata pendek (*k-tuples* / $W$-mers panjang 3 untuk protein, 11 untuk DNA) berbobot tinggi di atas threshold $T$, kemudian memperluas segmen tanpa gap (*High-scoring Segment Pairs / HSP*) ([Altschul et al. - Basic Local Alignment Search Tool](https://www.sciencedirect.com/science/article/pii/S0022283605803602)).

3. **Arsitektur AlphaFold Evoformer & Frame Representation**:
AlphaFold memodelkan rantai residu protein sebagai koordinat kerangka kaku spasial (Rigid Body Frames) $T_i = (R_i, \vec{x}_i) \in SE(3)$ yang mewakili orientasi grup peptida di ruang 3D ([Jumper et al. Nature 2021](https://www.nature.com/articles/s41586-021-03819-2)):
$$\mathcal{L}_{\text{FAPE}} = \frac{1}{N_{\text{frames}} N_{\text{atoms}}} \sum_{i, j} \min\left( d_{\text{clamp}}, \| T_i^{-1} \vec{x}_j - (T_i^{\text{true}})^{-1} \vec{x}_j^{\text{true}} \| \right)$$
Fungsi Frame Aligned Point Error (FAPE) invariant terhadap rotasi dan translasi global sistem koordinat Euclidean.""",
        "internals": r"""Aliran arsitektur komputasi prediksi struktur 3D protein dari sekuens mentah pada AlphaFold:

```mermaid
flowchart TD
    Seq["Sekuens Asam Amino Primer"] --> MSA_Engine["Pencarian Database Genetik -> Multiple Sequence Alignment (MSA)"]
    Seq --> Pair_Engine["Pencarian Template Template Struktur"]
    
    MSA_Engine & Pair_Engine --> Evoformer["Modul Evoformer: Komunikasi 48 Blok (MSA Representation <--> Residue Pair Representation)"]
    
    Evoformer --> StructureModule["Structure Module: 3D Invariant Point Attention (IPA)"]
    StructureModule --> PDB["Struktur Koordinat Atom 3D Final (PDB Format)"]
```

Evoformer memanfaatkan ko-evolusi spasial: jika dua residu asam amino saling berdekatan dalam lipatan 3D fisik, mutasi pada satu residu akan disertai oleh mutasi kompensasi pada residu pasangannya di sepanjang sejarah evolusi spesies ([AlphaFold Technical Method](https://www.nature.com/articles/s41586-021-03819-2)).""",
        "code_block": r"""```python
import numpy as np

# 1. Implementasi Algoritma Smith-Waterman untuk Penyejajaran Sekuens Genomik Lokal
def smith_waterman(seq1, seq2, match=2, mismatch=-1, gap=-2):
    n, m = len(seq1), len(seq2)
    H = np.zeros((n + 1, m + 1), dtype=int)
    
    max_score = 0
    max_pos = (0, 0)
    
    # Isi Matriks Skor Pemrograman Dinamis
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            score_diag = H[i-1, j-1] + (match if seq1[i-1] == seq2[j-1] else mismatch)
            score_up = H[i-1, j] + gap
            score_left = H[i, j-1] + gap
            H[i, j] = max(0, score_diag, score_up, score_left)
            
            if H[i, j] > max_score:
                max_score = H[i, j]
                max_pos = (i, j)
                
    # Backtracking dari Sel Bernilai Maksimum
    aligned1, aligned2 = [], []
    curr_i, curr_j = max_pos
    
    while curr_i > 0 and curr_j > 0 and H[curr_i, curr_j] > 0:
        val = H[curr_i, curr_j]
        diag = H[curr_i - 1, curr_j - 1]
        left = H[curr_i, curr_j - 1]
        up = H[curr_i - 1, curr_j]
        
        score_diff = match if seq1[curr_i - 1] == seq2[curr_j - 1] else mismatch
        if val == diag + score_diff:
            aligned1.append(seq1[curr_i - 1])
            aligned2.append(seq2[curr_j - 1])
            curr_i -= 1
            curr_j -= 1
        elif val == up + gap:
            aligned1.append(seq1[curr_i - 1])
            aligned2.append('-')
            curr_i -= 1
        else:
            aligned1.append('-')
            aligned2.append(seq2[curr_j - 1])
            curr_j -= 1
            
    return "".join(reversed(aligned1)), "".join(reversed(aligned2)), max_score

# Uji Coba Penyejajaran Dua Fragmen DNA
dna_a = "TGTTACGG"
dna_b = "GGTTGACTA"
aln_a, aln_b, score = smith_waterman(dna_a, dna_b)

print(f"Skor Alignment Lokal Terbaik: {score}")
print(f"Sekuens A Terjajar : {aln_a}")
print(f"Sekuens B Terjajar : {aln_b}")
```""",
        "pitfalls": r"""*Over-reliance pada pLDDT Score Tanpa Memperhatikan PDB PAE Matrix*: Pada AlphaFold, skor pLDDT (Predicted Local Distance Difference Test, rentang 0-100) hanya mengukur kepercayaan konformasi lokal setiap residu residu individual. Residu dengan skor pLDDT tinggi ($>80$) tetap bisa memiliki kesalahan orientasi spasial relatif yang masif terhadap domain lain. Selalu validasi matriks Predicted Aligned Error (PAE) untuk mengukur ketidakpastian posisi relatif antar domain protein ([Varadi et al. - AlphaFold Protein Structure Database](https://academic.oup.com/nar/article/50/D1/D439/6430488)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip Python untuk menghitung persentase kandungan GC-content ($(\#G + \#C) / \text{Length} \times 100$) dan mencari open reading frames (ORF) yang diawali oleh kodon start `ATG` dan diakhiri oleh kodon stop (`TAA`, `TAG`, `TGA`) pada string DNA.
*Rubrik*: Output mencetak panjang sequence, kandungan GC, dan kandidat rantai polipeptida.

### Level 2 (Menengah)
Implementasikan algoritma penyejajaran global Needleman-Wunsch dengan model penalti *Affine Gap Penalty* ($W(k) = \text{Gap}_{\text{open}} + k \cdot \text{Gap}_{\text{extend}}$) menggunakan 3 matriks pemrograman dinamis ($M, I_x, I_y$).
*Rubrik*: Kode membedakan pembukaan gap baru dengan perpanjangan gap yang sudah ada secara matematis.

### Level 3 (Mahir)
Bangun modul komputasi metrik RMSD (Root-Mean-Square Deviation) dan FAPE (Frame Aligned Point Error) 3D dari nol untuk membandingkan dua file struktur protein format PDB: implementasikan algoritma rotasi optimal Kabsch (menggunakan dekomposisi SVD) untuk menyelaraskan dua awan koordinat atom secara absolut.
*Rubrik*: Menghitung nilai RMSD yang identik dengan perangkat lunak standar BioPython / PyMOL.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Highly Accurate Protein Structure Prediction with AlphaFold | John Jumper et al. (Google DeepMind) | [Nature 2021 Article](https://www.nature.com/articles/s41586-021-03819-2) | Arsitektur Lengkap Evoformer, Invariant Point Attention, Loss FAPE |
| Identification of Common Molecular Subsequences (Smith-Waterman) | T. F. Smith & M. S. Waterman | [Journal of Molecular Biology 1981](https://www.sciencedirect.com/science/article/pii/0022283681900875) | Algoritma Asli Pemrograman Dinamis Penyejajaran Lokal |
| Basic Local Alignment Search Tool (BLAST) | Stephen F. Altschul et al. (NIH NCBI) | [Journal of Molecular Biology 1990](https://www.sciencedirect.com/science/article/pii/S0022283605803602) | Heuristik Pencarian Database Genom Skala Besar Sub-Linier |
| Biological Sequence Analysis: Probabilistic Models of Proteins and Nucleic Acids | R. Durbin, S. Eddy, A. Krogh, G. Mitchison | [Cambridge University Press](https://www.cambridge.org/core/books/biological-sequence-analysis/AA56B5D71C1720FEFFCA64700FE4B127) | Model Markov Tersembunyi (HMM) Profil Genomik, Matriks BLOSUM |"""
    },
    200: {
        "intuition": r"""Pernahkah Anda berjalan pulang ke rumah sambil melamun memikirkan pekerjaan, tetapi kaki Anda bisa melangkah dengan sempurna, belok di gang yang tepat, dan sampai di depan pintu tanpa Anda sadari? Namun, ketika tiba-tiba ada teka-teki rumit seperti mengalikan $17 \times 24$ di kepala Anda, langkah kaki Anda melambat, pupil mata Anda melebar, dan seluruh fokus Anda tersedot habis.

Psikolog Daniel Kahneman merumuskan arsitektur ini sebagai **Teori Dua Sistem Pikiran (Dual-Process Theory)** ([Kahneman - Thinking, Fast and Slow](https://us.macmillan.com/books/9780374533557/thinkingfastandslow)):
* **Sistem 1 (Fast, Otomatis, Intuitif)**: Bekerja instan tanpa usaha sadar, mengandalkan asosiasi pola masa lalu (seperti refleks menghindar dari bola yang melayang ke arah muka).
* **Sistem 2 (Slow, Sadar, Analitis)**: Mesin penalaran logika berkecepatan lambat yang membutuhkan konsentrasi penuh dan mengonsumsi energi mental tinggi.

Bagaimana otak mengingat hal yang sedang dipikirkan? Alan Baddeley memodelkannya sebagai **Memori Kerja (Working Memory)**: papan tulis mental sementara berkapasitas sangat terbatas yang dapat menampung informasi saat kita memecahkan masalah ([Baddeley - Working Memory](https://academic.oup.com/book/25442)).""",
        "theory": r"""Formulasi Formal Psikologi Kognitif & Arsitektur Pikiran:

1. **Model Memori Kerja Multi-Komponen Baddeley & Hitch (1974/2000)**:
Terdiri dari 4 subsistem koordinasi kognitif:
* **Central Executive**: Pengendali perhatian fokus utama, mengalokasikan sumber daya mental dan menekan gangguan (*inhibition*).
* **Phonological Loop**: Buffer penampung informasi berbasis bahasa dan akustik dengan loop artikulatoris verbal (kapasitas $\approx 2$ detik pengucapan vokal).
* **Visuospatial Sketchpad**: Buffer visual untuk memanipulasi citra spasial 2D/3D di dalam benak.
* **Episodic Buffer**: Integrator multimodal yang menggabungkan informasi visual, spasial, dan verbal dengan stempel waktu memori jangka panjang (*Long-Term Memory*).

2. **Persepsi Top-Down vs Bottom-Up (Pemodelan Bayesian)**:
Persepsi sadar $\hat{S}$ adalah estimasi Maximum A Posteriori (MAP) yang mengintegrasikan sinyal stimulus sensori fisik dari lingkungan luar (*bottom-up evidence* $p(E \mid S)$) dengan ekspektasi pengetahuan dan konteks masa lalu (*top-down prior* $p(S)$):
$$\hat{S} = \arg\max_S p(S \mid E) = \arg\max_S \frac{p(E \mid S) p(S)}{p(E)}$$
Jika stimulus sensori terdegradasi (misal kabut atau tulisan kabur), sistem kognitif bergantung penuh pada prior top-down ([Gregory - Perceptions as Hypotheses](https://royalsocietypublishing.org/doi/10.1098/rstb.1980.0090)).

3. **Batas Kapasitas Memori Kerja George Miller (The Magical Number 7 $\pm$ 2)**:
Kapasitas kanal manusia memproses informasi unidimensional dibatasi oleh kapasitas chunking diskret: $7 \pm 2$ chunks informasi, yang kemudian direvisi oleh Cowan (2001) menjadi sekitar $4 \pm 1$ chunks aktif dalam ketiadaan latihan rehearsal ([Cowan - The Magical Mystery Four](https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/magical-number-4-in-shortterm-memory-a-reconsideration-of-mental-storage-capacity/36E56BFBA69D0445ECBF33FBE809EF44)).""",
        "internals": r"""Arsitektur interaksi modul Memori Kerja Baddeley dengan Long-Term Memory:

```mermaid
flowchart TD
    CentralExec["Central Executive (Alokasi Perhatian & Kontrol Eksekutif)"]
    
    Phono["Phonological Loop (Bahasa & Buffer Verbal Akustik)"]
    Visuo["Visuospatial Sketchpad (Objek Spasial & Citra Visual)"]
    Episodic["Episodic Buffer (Integrasi Waktu & Pengalaman Multimodal)"]
    
    CentralExec <--> Phono
    CentralExec <--> Visuo
    CentralExec <--> Episodic
    
    LTM["Long-Term Memory (Memori Semantik, Episodik, Prosedural)"]
    Episodic <--> LTM
```

Sistem 1 pada manusia beroperasi seperti deep neural network feedforward (pencocokan pola embedding cepat), sedangkan Sistem 2 beroperasi seperti algoritma pencarian pohon Monte Carlo / Chain-of-Thought (penalaran bertahap dengan verifikasi kendala) ([Kahneman Nobel Lecture](https://www.nobelprize.org/prizes/economic-sciences/2002/kahneman/lecture/)).""",
        "code_block": r"""```python
import time

# 1. Simulasi Kognitif Sederhana: Efek Stroop (Stroop Effect Simulation)
# Mengukur konflik kompetisi antara Sistem 1 (Membaca Teks Otomatis) vs Sistem 2 (Menyebut Warna Tinta)

stimuli = [
    {"word": "MERAH", "color": "MERAH", "congruent": True},
    {"word": "HIJAU", "color": "HIJAU", "congruent": True},
    {"word": "BIRU",  "color": "MERAH", "congruent": False}, # Konflik Sistem 1 vs 2!
    {"word": "KUNING", "color": "HIJAU", "congruent": False} # Konflik Sistem 1 vs 2!
]

def simulate_reaction_time(stimulus):
    # Base processing time Sistem 1 persepsi warna
    base_rt = 300.0 # ms
    if not stimulus["congruent"]:
        # Penalti interferensi inhibisi kognitif Central Executive Sistem 2
        inhibition_cost = 220.0 # ms
        return base_rt + inhibition_cost
    return base_rt

congruent_rts = [simulate_reaction_time(s) for s in stimuli if s["congruent"]]
incongruent_rts = [simulate_reaction_time(s) for s in stimuli if not s["congruent"]]

print("Simulasi Kognitif Efek Stroop:")
print(f"Rata-rata Reaksi Kongruen  (Tanpa Konflik) : {sum(congruent_rts)/len(congruent_rts):.1f} ms")
print(f"Rata-rata Reaksi Inkongruen (Dengan Konflik): {sum(incongruent_rts)/len(incongruent_rts):.1f} ms")
print(f"Biaya Interferensi Kognitif (Stroop Interference Cost): {(sum(incongruent_rts) - sum(congruent_rts))/2:.1f} ms")
```""",
        "pitfalls": r"""*Bias Konfirmasi dan Anchoring Heuristic pada Sistem 1*: Ketergantungan berlebihan pada heuristik ketersediaan (*availability heuristic*) membuat manusia secara sistematis menempel pada angka acak pertama yang dilihat (*anchoring effect*) atau hanya mencari informasi yang membenarkan hipotesis awal mereka (*confirmation bias*). Dalam perancangan sistem interaksi manusia-komputer dan AI, antarmuka harus dirancang secara sengaja untuk memicu refleksi kritis Sistem 2 pada keputusan-keputusan berisiko tinggi ([Tversky & Kahneman - Judgment under Uncertainty](https://www.science.org/doi/10.1126/science.185.4157.1124)).""",
        "exercises": r"""### Level 1 (Pemula)
Rancang eksperimen pengukuran memori kerja menggunakan tugas *Digit Span Test* (maju dan mundur): catat kapasitas retensi maksimum subjek manusia atau partisipan uji coba, dan analisis apakah hasilnya memvalidasi hukum Miller $7 \pm 2$.
*Rubrik*: Laporan data eksperimen menyajikan rata-rata digit span dan deviasi standar.

### Level 2 (Menengah)
Bangun model komputasional *Drift-Diffusion Model (DDM)* untuk keputusan biner 2-pilihan:
$$dx = v \cdot dt + \sigma \cdot dW$$
Simulasikan akumulasi bukti sensori dari waktu ke waktu hingga menyentuh batas keputusan atas ($+a$) atau bawah ($-a$). Plot distribusi waktu reaksi (*reaction time distribution*) yang dihasilkan.
*Rubrik*: Bentuk kurva waktu reaksi terdistribusi miring ke kanan (*right-skewed Wald distribution*).

### Level 3 (Mahir)
Implementasikan simulasi komputasional arsitektur kognitif modular ACT-R atau SOAR mini di Python: rancang modul declarative memory (pencarian fakta berbasis spreading activation), modul procedural memory (aturan produksi IF-THEN dengan resolusi konflik utilitas), dan buktikan kemampuan model memecahkan tugas navigasi labirin bertingkat.
*Rubrik*: Model mengeksekusi siklus kognitif lengkap (Goal -> Match -> Resolve -> Fire).""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Thinking, Fast and Slow | Daniel Kahneman (Nobel Laureate) | [Farrar, Straus and Giroux](https://us.macmillan.com/books/9780374533557/thinkingfastandslow) | Teori Sistem 1 vs Sistem 2, Heuristik Kognitif & Bias |
| Working Memory (Oxford Psychology Series) | Alan Baddeley | [Oxford University Press](https://academic.oup.com/book/25442) | Model Multi-Komponen Memori Kerja, Central Executive |
| Judgment under Uncertainty: Heuristics and Biases | Amos Tversky & Daniel Kahneman | [Science 1974 Classic](https://www.science.org/doi/10.1126/science.185.4157.1124) | Landasan Asli Sains Pengambilan Keputusan Manusia |
| The Magical Number Seven, Plus or Minus Two | George A. Miller (Harvard University) | [Psychological Review 1956](https://psycnet.apa.org/record/1957-02914-001) | Batas Kapasitas Pemrosesan Informasi Pikiran Manusia |"""
    },
    201: {
        "intuition": r"""Mengapa sebuah kalimat seperti *"Kucing mengejar tikus hitam"* terdengar alami dan benar, sedangkan *"Hitam tikus kucing mengejar"* terdengar berantakan seperti sampah kata? Dan bagaimana sebuah komputer bisa membedakan makna ganda dari kalimat *"Saya melihat pria dengan teropong"* (apakah saya yang memakai teropong, atau pria itu yang sedang memegang teropong)?

Bahasa manusia bukanlah sekadar deretan kata yang dijejerkan seperti gerbong kereta. Bahasa manusia memiliki struktur pohon hierarki yang sangat rapi dan berulang tanpa henti (**Rekursi**) ([Chomsky - Syntactic Structures](https://www.degruyter.com/document/doi/10.1515/9783112316009/html)).

**Linguistik Formal & Komputasional** adalah ilmu membedah anatomi bahasa manusia menggunakan matematika dan logika simbolik:
1. **Fonetik & Fonologi**: Ilmu tentang gelombang fisik suara dan pengucapan fonem.
2. **Morfologi**: Ilmu tentang bagaimana kata dasar dirangkai dengan imbuhan (misal: *ajar* $\to$ *belajar*, *pengajaran*).
3. **Sintaksis**: Aturan tata bahasa formal yang menyusun kata menjadi pohon frasa (**Context-Free Grammar / CFG**).
4. **Semantik & Pragmatik**: Logika makna hakiki dari sebuah proposisi dan bagaimana konteks situasi sosial mengubah arti kalimat tersebut ([Jurafsky & Martin - Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/)).""",
        "theory": r"""Formulasi Matematis Tata Bahasa Formal & Semantik:

1. **Hierarki Tata Bahasa Noam Chomsky**:
Tata Bahasa Formal didefinisikan sebagai tuple $G = \langle V, \Sigma, R, S \rangle$:
* **Tipe 3 (Reguler)**: $A \to aB$ atau $A \to a$ (Dikenali oleh *Finite State Automata* / Regex).
* **Tipe 2 (Context-Free Grammar / CFG)**: $A \to \alpha$ di mana $A \in V$ dan $\alpha \in (V \cup \Sigma)^*$ (Dikenali oleh *Pushdown Automata*, memodelkan struktur pohon sintaksis bahasa manusia).
* **Tipe 1 (Context-Sensitive Grammar)**: $\alpha A \beta \to \alpha \gamma \beta$.
* **Tipe 0 (Turing Unrestricted)**: Mesin Turing universal ([Hopcroft, Motwani, Ullman - Automata Theory](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-automata-theory-languages-and-computation/P200000003348)).

2. **Algoritma Parsing Cocke-Younger-Kasami (CYK)**:
Mem-parsing kalimat panjang $n$ di bawah CFG dalam bentuk normal Chomsky (*Chomsky Normal Form / CNF* di mana semua aturan berupa $A \to BC$ atau $A \to a$) via Dynamic Programming matriks segitiga:
$$P[i, j, A] = \bigvee_{k=1}^{j-1} \bigvee_{A \to B C} \left( P[i, k, B] \land P[i+k, j-k, C] \right)$$
Kompleksitas komputasi eksak $\mathcal{O}(n^3 |R|)$, menjamin pencarian pohon sintaksis parsing bebas galat.

3. **Semantik Komposisional Formal Montague**:
Prinsip Gottlob Frege: Arti dari keseluruhan kalimat adalah fungsi matematis dari arti bagian-bagian komponennya. Menggunakan Kalkulus Lambda bertipe ($\lambda$-Calculus):
$$\text{"mengejar"} = \lambda y. \lambda x. \text{Chases}(x, y)$$
$$\text{"tikus"} = \text{Mouse}, \quad \text{"mengejar tikus"} = (\lambda y. \lambda x. \text{Chases}(x, y))(\text{Mouse}) = \lambda x. \text{Chases}(x, \text{Mouse})$$
$$\text{"kucing"} = \text{Cat}, \quad \text{"kucing mengejar tikus"} = (\lambda x. \text{Chases}(x, \text{Mouse}))(\text{Cat}) = \text{Chases}(\text{Cat}, \text{Mouse})$$""",
        "internals": r"""Struktur internal pohon parsing sintaksis Context-Free Grammar (Parse Tree) untuk kalimat ambigu:

```mermaid
flowchart TD
    S["S (Kalimat)"] --> NP["NP (Frasa Benda): 'Saya'"]
    S --> VP["VP (Frasa Kerja)"]
    VP --> V["V: 'melihat'"]
    VP --> NP2["NP (Frasa Benda)"]
    NP2 --> NP3["NP: 'pria'"]
    NP2 --> PP["PP (Frasa Preposisi)"]
    PP --> P["P: 'dengan'"]
    PP --> NP4["NP: 'teropong'"]
```

Ketika struktur pohon parsing dibangun, ambiguitas semantik dapat diselesaikan secara komputasional dengan membandingkan probabilitas probilistik CFG (*PCFG*) dari kedua variasi pohon yang terbentuk ([Manning & Schütze - Foundations of Statistical NLP](https://nlp.stanford.edu/fsnlp/)).""",
        "code_block": r"""```python
# Implementasi Algoritma Parsing CYK (Cocke-Younger-Kasami) Sederhana
def cyk_parse(words, grammar):
    n = len(words)
    # Tabel DP segitiga: table[i][j] berisi set simbol non-terminal yang mencakup kata i s/d i+j
    table = [[set() for _ in range(n + 1)] for _ in range(n + 1)]
    
    # 1. Base Case: Aturan Terminal (A -> kata)
    for i in range(1, n + 1):
        word = words[i - 1]
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                if len(rhs) == 1 and rhs[0] == word:
                    table[i][1].add(lhs)
                    
    # 2. Dynamic Programming: Gabungkan span panjang l dari 2 s/d n
    for l in range(2, n + 1): # Panjang span
        for i in range(1, n - l + 2): # Titik mulai span
            for k in range(1, l): # Titik pembagian span
                # Cek kombinasi table[i][k] dan table[i+k][l-k]
                left_symbols = table[i][k]
                right_symbols = table[i + k][l - k]
                
                for lhs, rhs_list in grammar.items():
                    for rhs in rhs_list:
                        if len(rhs) == 2:
                            B, C = rhs[0], rhs[1]
                            if B in left_symbols and C in right_symbols:
                                table[i][l].add(lhs)
                                
    # Kalimat valid jika simbol awal 'S' ada di table[1][n]
    return 'S' in table[1][n]

# Tata Bahasa Sederhana dalam Bentuk Normal Chomsky (CNF)
grammar = {
    'S':  [['NP', 'VP']],
    'VP': [['V', 'NP']],
    'NP': [['Det', 'N'], ['saya']],
    'V':  [['makan']],
    'Det':[['sebuah']],
    'N':  [['apel']]
}

sentence = ["saya", "makan", "sebuah", "apel"]
is_valid = cyk_parse(sentence, grammar)
print(f"Kalimat: '{' '.join(sentence)}'")
print(f"Hasil Parsing Formal CYK: {'VALID (Gramatikal)' if is_valid else 'TIDAK VALID'}")
```""",
        "pitfalls": r"""*Ledakan Kombinatorial Ambiguitas Parsing (Combinatorial Ambiguity)*: Pada kalimat panjang di dunia nyata dengan banyak frasa preposisi bertumpuk (seperti *"Dia meletakkan buku di atas meja di samping lampu di dekat jendela"*), jumlah kemungkinan pohon parsing yang valid secara gramatikal tumbuh secara eksponensial mengikuti bilangan Catalan $C_n = \frac{1}{n+1}\binom{2n}{n}$. Parsing berbasis aturan kaku murni runtuh; parser modern harus menggunakan bobot probabilitas (PCFG) atau transformer neural parser ([Jurafsky & Martin Chapter 13](https://web.stanford.edu/~jurafsky/slp3/)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis mesin Transduser Keadaan Terbatas (*Finite State Transducer / FST*) sederhana di Python untuk memodelkan proses morfologi pembentukan kata kerja bahasa Indonesia: aturan prefiks *meN-* (*tulis* $\to$ *menulis*, *baca* $\to$ *membaca*, *sapu* $\to$ *menyapu*).
*Rubrik*: FST menangani fenomena peleburan fonem huruf k, p, t, s dengan benar.

### Level 2 (Menengah)
Bangun implementasi Probabilistic Context-Free Grammar (PCFG) Parser menggunakan algoritma Viterbi-CYK: berikan bobot probabilitas $\log P(A \to BC)$ pada setiap aturan tata bahasa, dan temukan pohon parsing sintaksis tunggal yang memiliki probabilitas maksimum untuk kalimat ambigu.
*Rubrik*: Output mengembalikan struktur pohon parsing berprobabilitas tertinggi secara deterministik.

### Level 3 (Mahir)
Implementasikan sistem Semantik Komposisional berbasis evaluasi ekspresi $\lambda$-Kalkulus murni di Python: representasikan kata benda sebagai konstanta entitas, kata sifat sebagai fungsi predikat biner, dan lakukan reduksi $\beta$ (*beta-reduction*) langkah demi langkah hingga menghasilkan ekspresi logika orde pertama (First-Order Logic) yang dapat dievaluasi kebenarannya terhadap basis data fakta dunia miniatur.
*Rubrik*: Berhasil memproses kalimat seperti "Semua anjing menggonggong" menjadi $\forall x (\text{Dog}(x) \to \text{Barks}(x))$.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Speech and Language Processing (3rd Ed. Draft) | Dan Jurafsky & James H. Martin (Stanford) | [Jurafsky SLP3 Textbook](https://web.stanford.edu/~jurafsky/slp3/) | Alkitab Pemrosesan Bahasa Alami: CFG, Parsing CYK, Semantik |
| Syntactic Structures | Noam Chomsky (MIT) | [De Gruyter Mouton Classic](https://www.degruyter.com/document/doi/10.1515/9783112316009/html) | Teori Tata Bahasa Generatif Transformasional Asli |
| Introduction to Automata Theory, Languages, and Computation | John E. Hopcroft, Rajeev Motwani, Jeffrey D. Ullman | [Pearson Education](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-automata-theory-languages-and-computation/P200000003348) | Hierarki Chomsky, Teori Otomata, Gramatika Bebas Konteks |
| Foundations of Statistical Natural Language Processing | Christopher D. Manning & Hinrich Schütze | [MIT Press NLP Book](https://nlp.stanford.edu/fsnlp/) | Pendekatan Statistik Parsing Sintaksis, N-gram, Model PCFG |"""
    }
}
