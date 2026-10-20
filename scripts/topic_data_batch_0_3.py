# scripts/topic_data_batch_0_3.py
"""
Rich technical content database for Batch 1: Topics 1 to 52.
"""

BATCH_0_3_DATA = {
    1: {
        "intuition": """
Bayangkan otak Anda seperti sebuah komputer dengan RAM terbatas dan hard drive yang sangat besar. Ketika Anda membaca buku atau menonton video tutorial, informasi baru hanya masuk ke "RAM sementara" (working memory). Jika RAM tidak segera disimpan ke hard drive permanen (Long-Term Memory) melalui metode yang tepat, informasi tersebut akan lenyap tersapu dalam waktu kurang dari 24 jam (Fenomena Ebbinghaus Forgetting Curve).

Meta-learning adalah ilmu tentang "bagaimana cara merancang BIOS dan algoritma kompresi data terbaik untuk otak Anda sendiri". Bukannya menghafal secara pasif (re-reading) yang menimbulkan ilusi kompetensi (*illusion of explanatory depth*), meta-learning memaksa otak melakukan penarikan informasi aktif (*active recall*) dan konsolidasi sinapsis terencana.
""",
        "theory": """
### 1. Kurva Retensi Ebbinghaus & Spaced Repetition
Retensi memori manusia dimodelkan secara matematis dengan fungsi eksponensial negatif:
$$R(t) = e^{-\\frac{t}{S}}$$
Di mana:
- $R(t)$ adalah probabilitas mengingat kembali (*retrieval probability*) pada waktu $t$.
- $S$ adalah kekuatan memori (*memory stability*), yang berbanding lurus dengan jumlah pengulangan aktif pada interval waktu yang tepat.

Ketika pengulangan dilakukan tepat saat $R(t) \\approx 0.9$, kekuatan stabilitas baru $S_{n+1}$ melonjak secara eksponensial:
$$S_{n+1} = S_n \\cdot (1 + a \\cdot e^{-b \\cdot R})$$

### 2. Algoritma SM-2 (SuperMemo-2)
Algoritma penjadwalan kartu memori Spaced Repetition mendasarkan perhitungan interval $I(n)$ dan faktor kemudahan (*Ease Factor* $EF$):
$$EF' = EF + (0.1 - (5 - q) \\cdot (0.08 + (5 - q) \\cdot 0.02))$$
$$I(1) = 1, \\quad I(2) = 6, \\quad I(n) = I(n-1) \\times EF$$
Di mana $q \\in [0, 5]$ adalah skor kualitas penarikan memori pengguna.
""",
        "internals": """
```mermaid
flowchart TD
    A["Stimulus Belajar Baru"] --> B["Sensory Memory (< 1 detik)"]
    B --> C["Working Memory (RAM Otak: 4-7 Chunks)"]
    C -->|Passive Reading| D["Lupa / Overwritten (< 24 jam)"]
    C -->|Feynman Technique + Active Retrieval| E["Hippocampus (Encoding)"]
    E -->|Spaced Repetition Sleep Cycles| F["Neocortex (Long-Term Memory Sinaptik)"]
    F -->|Retrieval Practice| C
```
Proses biologis konsolidasi memori bergantung pada **Long-Term Potentiation (LTP)** di mana reseptor NMDA diaktifkan, memicu masuknya ion kalsium $Ca^{2+}$, yang menginstruksikan sintesis protein untuk memperkuat koneksi sinapsis antar neuron.
""",
        "code_block": """```python
import math
from dataclasses import dataclass

@dataclass
class FlashcardReview:
    repetition: int
    interval_days: float
    ease_factor: float

def calculate_sm2(quality: int, card: FlashcardReview) -> FlashcardReview:
    \"\"\"
    Implementasi murni algoritma SuperMemo-2 (SM-2) untuk spaced repetition.
    quality: 0 (blackout total) s/d 5 (sempurna tanpa jeda)
    \"\"\"
    if quality < 0 or quality > 5:
        raise ValueError("Skor kualitas harus antara 0 dan 5.")
        
    # Perbarui Ease Factor
    new_ef = card.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ef = max(1.3, new_ef)  # Batas bawah stabilitas SM-2
    
    if quality < 3:
        # Gagal mengingat: reset siklus repetisi
        return FlashcardReview(repetition=0, interval_days=1.0, ease_factor=new_ef)
    else:
        # Berhasil mengingat
        if card.repetition == 0:
            next_interval = 1.0
        elif card.repetition == 1:
            next_interval = 6.0
        else:
            next_interval = math.ceil(card.interval_days * new_ef)
            
        return FlashcardReview(
            repetition=card.repetition + 1,
            interval_days=next_interval,
            ease_factor=new_ef
        )

# Contoh Simulasi Pembelajaran 4 Putaran
card = FlashcardReview(repetition=0, interval_days=1.0, ease_factor=2.5)
ratings = [4, 5, 4, 5]
print("Simulasi Penjadwalan Pengulangan (Spaced Repetition):")
for day_idx, score in enumerate(ratings, 1):
    card = calculate_sm2(score, card)
    print(f"Sesi {day_idx}: Nilai={score} -> Interval Berikutnya: {card.interval_days:.0f} hari (EF={card.ease_factor:.2f})")
```""",
        "pitfalls": """
1. **The Highlighting / Re-reading Trap**: Menstabilkan teks buku atau menonton video ulang berulang kali hanya memicu *fluency illusion* (merasa paham karena konten tampak familiar, padahal neuron otak tidak mampu merekonstruksi konsep tersebut tanpa melihat teks).
2. **Cramming (Belajar Semalam Suntuk)**: Menumpuk 10 jam dalam 1 malam menciptakan spiking memori instan yang akan terhapus 85% dalam 72 jam karena tidak ada fase konsolidasi tidur REM dan *slow-wave sleep*.
3. **Chunking Failure**: Mencoba menghafal detail mikroskopis sebelum memahami kerangka pohon pengetahuan (*knowledge tree*) secara holistik.
""",
        "exercises": """
### Level 1 (Dasar)
Gunakan teknik Feynman untuk menjelaskan konsep `Pointer di Bahasa C` atau `Resistansi Listrik` kepada anak berusia 10 tahun tanpa menggunakan istilah teknis sama sekali. Tulis dalam 3 paragraf sederhana.

### Level 2 (Menengah)
Bangun sistem pelacakan Spaced Repetition mandiri menggunakan Python CLI atau Anki deck yang mengimplementasikan pemisahan kartu memori menjadi "Konsep Teoretis", "Algoritma", dan "Perintah Shell".

### Level 3 (Mahir)
Rancang arsitektur sistem *knowledge retrieval engine* pribadi berbasis Obsidian / Markdown berkoneksi dua arah (bi-directional linking / Zettelkasten) yang mengintegrasikan pengujian aktif harian otomatis via skrip Python.
""",
        "references": """
- Brown, P. C., Roediger, H. L., & McDaniel, M. A. (2014). *Make It Stick: The Science of Successful Learning*. Harvard University Press.
- Oakley, B. (2014). *A Mind for Numbers: How to Excel at Math and Science*. TarcherPerigee.
- Wozniak, P. A. (1990). *Optimization of learning: A new approach to spaced repetition*. University of Technology in Poznan.
"""
    },
    2: {
        "intuition": """
Bayangkan Anda ingin membuat mobil balap. Cara berpikir kebanyakan orang adalah melihat mobil yang sudah ada (Ferrari, Porsche) lalu meniru bentuknya dengan sedikit modifikasi warna atau bemper (penalaran analogi). 

Sebaliknya, **First-Principles Thinking (Penalaran Prinsip Pertama)** membongkar mobil itu hingga ke tingkat atom dan hukum fisika: Berapa berat material aluminium per kilogram? Berapa kapasitas pembakaran hidrokarbon atau densitas energi sel litium? Berapa koefisien gaya gesek ban terhadap aspal? Setelah Anda mendapatkan kebenaran paling dasar yang tidak dapat dibantah lagi, barulah Anda merakit ulang solusi baru yang jauh lebih efisien dari nol.
""",
        "theory": """
Prinsip pertama berakar dari epistemologi Aristoteles: *arche* (prinsip awal yang darinya suatu hal pertama kali diketahui dan tidak dapat dibuktikan dari prinsip lain yang lebih mendasar).

Secara metodologis, dekonstruksi masalah mengikuti langkah:
1. **Identifikasi Asumsi Terselubung**: Misalkan $A = \\{a_1, a_2, \\dots, a_n\\}$ adalah himpunan klaim umum industri.
2. **Uji Reduksi**: Untuk setiap $a_i$, tanyakan: Apakah $a_i$ adalah hukum alam semesta (fisika/matematika) atau sekadar konvensi historis / tradisi sosial?
$$a_i \\in \\mathcal{L}_{fundamental} \\quad \\text{vs} \\quad a_i \\in \\mathcal{C}_{konvensi}$$
3. **Formulasi Ulang**: Rekonstruksi solusi hanya menggunakan elemen dari $\\mathcal{L}_{fundamental}$:
$$S_{baru} = f(\\mathcal{L}_{fundamental})$$
""",
        "internals": """
```mermaid
graph TD
    Problem["Masalah Kompleks: Biaya Roket Terlalu Mahal"] --> Analogi["Penalaran Berbasis Analogi: Beli roket buatan Rusia seharga $65 juta"]
    Problem --> FirstPrinciple["Penalaran Prinsip Pertama"]
    FirstPrinciple --> Decomp["Dekomposisi Bahan Baku: Paduan Al-Li, Titanium, Serat Karbon, Propelan"]
    Decomp --> MarketPrice["Hitung Harga Komoditas Logam: Hanya 2% dari total harga roket jadi"]
    MarketPrice --> Synthesis["Sintesis Solusi: Bangun manufaktur internal & roket pakai-ulang (SpaceX)"]
```
""",
        "code_block": """```python
def first_principles_cost_audit(components: list[dict]) -> dict:
    \"\"\"
    Dekonstruksi biaya produk menjadi bahan mentah fundamental vs markup proses industri.
    \"\"\"
    raw_material_cost = sum(c['raw_cost'] * c['weight_kg'] for c in components)
    market_selling_price = sum(c['commercial_price'] for c in components)
    
    markup_factor = market_selling_price / max(1e-6, raw_material_cost)
    theoretical_savings = market_selling_price - raw_material_cost
    
    return {
        "total_raw_material_cost": raw_material_cost,
        "market_selling_price": market_selling_price,
        "markup_multiplier": round(markup_factor, 2),
        "theoretical_maximum_margin": round(theoretical_savings, 2)
    }

# Simulasi baterai pack industri
battery_bill_of_materials = [
    {"name": "Nickel", "weight_kg": 30, "raw_cost": 16.5, "commercial_price": 1200},
    {"name": "Cobalt", "weight_kg": 5, "raw_cost": 32.0, "commercial_price": 500},
    {"name": "Lithium Carbonate", "weight_kg": 12, "raw_cost": 14.0, "commercial_price": 900},
    {"name": "Aluminum Casings", "weight_kg": 40, "raw_cost": 2.4, "commercial_price": 450},
    {"name": "Electrolyte & Separator", "weight_kg": 15, "raw_cost": 8.0, "commercial_price": 600}
]

audit = first_principles_cost_audit(battery_bill_of_materials)
print("Analisis Prinsip Pertama Struktur Biaya Baterai:")
for k, v in audit.items():
    print(f" - {k}: {v}")
```""",
        "pitfalls": """
1. **Menghabiskan Energi untuk Hal Trivial**: Menerapkan penalaran prinsip pertama untuk memilih warna baju atau hal sepele hanya membuang waktu. Gunakan prinsip pertama hanya saat taruhannya tinggi (*high-stakes*) atau ada inefisiensi masif di industri.
2. **Mengabaikan Hukum Termodinamika & Fisika Nyata**: Mendekonstruksi sistem tanpa memperhitungkan batas efisiensi Carnot, disipasi panas, atau hambatan material.
""",
        "exercises": """
### Level 1 (Dasar)
Pilih satu teknologi yang Anda gunakan sehari-hari (misal: Cloud Storage). Dekonstruksi biaya dan komponen dasarnya: berapa harga disk mentah per TB vs berapa harga sewa bulanan penyedia cloud?

### Level 2 (Menengah)
Lakukan dekonstruksi arsitektur software web tradisional: Mengapa kita butuh relasional database, caching layer, dan frontend terpisah? Jika dimulai dari batas latency jaringan dan RAM vs NVMe, apa arsitektur paling sederhana yang bisa melayani 100.000 QPS?

### Level 3 (Mahir)
Tulis makalah teknis internal (RFC) dekonstruksi algoritma training neural network: Mengapa gradient descent butuh matriks perkalian besar di GPU? Mengapa tidak memakai bitwise operations atau photonic chips?
""",
        "references": """
- Aristotle. *Posterior Analytics* (Buku I, Bagian 2).
- Musk, E. (2012). *Interview on First Principles and Physics Thinking*.
- Feynman, R. P. (1965). *The Character of Physical Law*. MIT Press.
"""
    },
    3: {
        "intuition": """
Ketika Anda menaikkan suhu pancuran air dingin, Anda memutar keran air panas. Karena pipa airnya panjang, air yang keluar masih dingin. Anda merasa kurang panas, jadi Anda memutar keran lebih jauh lagi. Lima detik kemudian, air mendidih keluar dan membakar kulit Anda! Anda panik dan memutar keran ke posisi paling dingin, hingga beberapa detik kemudian air menjadi es membeku.

Itulah **Systems Thinking**. Dunia nyata bukanlah garis lurus sebab-akibat sederhana ($A \\to B$), melainkan jaringan melingkar yang memiliki *delay* (tundaan waktu), *feedback loops* (umpan balik penguat atau penyeimbang), dan *emergence* (sifat baru yang muncul dari interaksi komponen yang tidak dimiliki komponen individu).
""",
        "theory": """
Model sistem dinamik matematis dirumuskan sebagai sistem persamaan diferensial non-linier:
$$\\frac{d\\mathbf{x}}{dt} = \\mathbf{f}(\\mathbf{x}(t), \\mathbf{u}(t), \\boldsymbol{\\theta})$$
Di mana:
- $\\mathbf{x}(t) \\in \\mathbb{R}^n$ adalah vektor *stocks* (akumulasi status sistem, misalnya memori, populasi, modal).
- $\\frac{d\\mathbf{x}}{dt}$ adalah *flows* (laju perubahan: inflow dikurangi outflow).
- Feedback loop positif (reinforcing loop, $R$) ditandai dengan nilai eigen Jacobian $\\lambda_i > 0$ yang memicu pertumbuhan eksponensial.
- Feedback loop negatif (balancing loop, $B$) ditandai dengan $\\lambda_i < 0$ yang menghasilkan osilasi teredam atau kestabilan dinamis (*homeostasis*).
""",
        "internals": """
```mermaid
graph LR
    subgraph Balancing Loop with Delay
        Target["Suhu Idaman (Goal)"] --> Error["Error = Target - Aktual"]
        Error --> Actuator["Putar Keran Panas"]
        Actuator -->|Delay Waktu Pipa| Stock["Suhu Air Aktual (Stock)"]
        Stock --> Error
    end
```
""",
        "code_block": """```python
import numpy as np

def simulate_shower_system(steps=60, delay_seconds=5, target_temp=40.0):
    \"\"\"
    Simulasi sistem kontrol suhu pancuran air dengan feedback delay.
    \"\"\"
    temp_history = [20.0] * (delay_seconds + 1)
    tap_setting = 20.0
    
    print(f"Target Suhu: {target_temp}°C | Delay Pipa: {delay_seconds} detik")
    print(f"{'Detik':<8}{'Setting Keran':<16}{'Suhu Keluar':<14}{'Status'}")
    
    for t in range(steps):
        # Suhu air yang keluar sekarang adalah akibat dari setting keran beberapa detik lalu
        current_temp = temp_history[-delay_seconds]
        error = target_temp - current_temp
        
        # Pengguna naif bereaksi secara proporsional terhadap error saat ini tanpa memperhitungkan delay
        tap_setting += 0.4 * error
        tap_setting = max(10.0, min(80.0, tap_setting))
        
        # Air baru mengalir ke pipa
        temp_history.append(tap_setting)
        
        if t % 5 == 0:
            status = "Stabil" if abs(error) < 1.0 else ("Terlalu Panas" if current_temp > target_temp else "Terlalu Dingin")
            print(f"{t:<8}{tap_setting:<16.1f}{current_temp:<14.1f}{status}")

simulate_shower_system()
```""",
        "pitfalls": """
1. **Linear Thinking in a Non-Linear World**: Memperbaiki kemacetan jalan raya dengan menambah jalur baru (Braess's Paradox: penambahan kapasitas justru menginduksi lebih banyak mobil sehingga kemacetan bertambah parah).
2. **Treating Symptoms Instead of Root Causes**: Memberikan obat penurun panas pada pasien infeksi bakteri tanpa memberikan antibiotik untuk membunuh sumber bakterinya.
""",
        "exercises": """
### Level 1 (Dasar)
Gambarkan diagram Causal Loop Diagram (CLD) untuk sistem "Cache Memory di Server Web": Tunjukkan hubungan antara *Cache Hit Ratio*, *Latency Database*, *Beban CPU*, dan *Kapasitas RAM*.

### Level 2 (Menengah)
Implementasikan simulasi predator-prey Lotka-Volterra menggunakan Python/NumPy untuk memodelkan interaksi dua populasi dengan osilasi siklus tertutup.

### Level 3 (Mahir)
Analisis fenomena *Cascading Failure* pada microservice architecture menggunakan model sistem dinamik: Tunjukkan bagaimana sebuah service lambat memicu thread exhaustion dan menumbangkan seluruh cluster.
""",
        "references": """
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green Publishing.
- Sterman, J. (2000). *Business Dynamics: Systems Thinking and Modeling for a Complex World*. McGraw-Hill.
- Senge, P. M. (1990). *The Fifth Discipline: The Art & Practice of The Learning Organization*. Doubleday.
"""
    },
    4: {
        "intuition": """
Bagaimana Anda tahu bahwa pernyataan "Semua angsa berwarna putih" adalah benar? Jika Anda melihat 10.000 angsa putih di Eropa, apakah itu membuktikan kebenaran absolut? Tidak! Cukup satu penemuan angsa hitam di Australia untuk menghancurkan seluruh teori tersebut.

Inilah inti dari **Filsafat Sains & Falsifikasi Karl Popper**: Sebuah teori ilmiah tidak pernah dapat "dibuktikan benar 100%" secara mutlak melalui verifikasi (induksi); ia hanya dapat dianggap sebagai penjelasan terbaik sementara yang *belum berhasil dibuktikan salah* (falsifikasi). Jika sebuah pernyataan tidak dapat diuji atau tidak memiliki skenario di mana ia bisa gagal, pernyataan tersebut bukanlah sains, melainkan dogma atau pseudosains.
""",
        "theory": """
### 1. Masalah Induksi (Hume's Problem)
Induksi menyimpulkan proposisi universal dari proposisi partikular:
$$\\forall i \\in \\{1, \\dots, N\\}, P(x_i) \\implies \\forall x, P(x)$$
David Hume membuktikan bahwa inferensi ini secara logis tidak valid, tidak peduli seberapa besar nilai $N$.

### 2. Kriteria Demarkasi Karl Popper
Teori $T$ bersifat ilmiah jika dan hanya jika ruang kejadian pengamatan empiris $\\Omega$ memuat himpunan bagian pengamatan potensial yang memalsukan $T$ ($F_T \\neq \\emptyset$):
$$\\exists e \\in \\Omega \\quad \\text{sedemikian sehingga} \\quad T \\land e \\vdash \\bot$$
""",
        "internals": """
```mermaid
flowchart TD
    Obs["Observasi Empiris Dunia Nyata"] --> Hyp["Formulasi Hipotesis Ilmiah (Harus Falsifiable)"]
    Hyp --> Exp["Desain Eksperimen Kritis (Mencari Bukti yang Menggagalkan)"]
    Exp -->|Hipotesis Gagal| Mod["Hipotesis Gugur / Diperbarui (Revisi Teori)"]
    Exp -->|Hipotesis Lolos| Corroborate["Teori Teruji Sementara (Corroborated, Bukan Fakta Mutlak)"]
    Corroborate --> Exp
    Mod --> Hyp
```
""",
        "code_block": """```python
import random

class HypothesisTester:
    \"\"\"
    Simulasi prinsip falsifikasi Popper:
    Mencari counterexample untuk meruntuhkan klaim universal.
    \"\"\"
    def __init__(self, rule_description, rule_fn):
        self.rule_description = rule_description
        self.rule_fn = rule_fn
        
    def test_falsifiability(self, test_generator, num_trials=10000):
        for trial in range(1, num_trials + 1):
            sample = test_generator()
            result = self.rule_fn(sample)
            if not result:
                return {
                    "falsified": True,
                    "counterexample": sample,
                    "trials_before_falsification": trial
                }
        return {
            "falsified": False,
            "counterexample": None,
            "trials_before_falsification": num_trials
        }

# Hipotesis Ilmiah: "Bilangan n^2 + n + 41 selalu menghasilkan bilangan prima untuk semua integer positif n"
# (Formula Euler klasik yang menghasilkan prima hingga n=39)
def is_prime(x):
    if x < 2: return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0: return False
    return True

tester = HypothesisTester(
    "Euler Formula generates primes",
    lambda n: is_prime(n**2 + n + 41)
)

result = tester.test_falsifiability(lambda: random.randint(1, 100), num_trials=5000)
print(f"Hasil Pengujian Falsifikasi: {result}")
```""",
        "pitfalls": """
1. **Confirmation Bias**: Peneliti seringkali secara tidak sadar hanya mencari data atau metrik yang mendukung hipotesis mereka, dan mengabaikan data anomali yang membantahnya.
2. **Unfalsifiable Claims**: Membuat hipotesis yang memiliki "alasan cadangan" untuk setiap kemungkinan hasil (misalnya: "Sistem saya gagal karena energi kosmik yang tidak terdeteksi").
""",
        "exercises": """
### Level 1 (Dasar)
Ambil sebuah bug software yang baru-baru ini Anda temukan. Tuliskan hipotesis ilmiah mengapa bug tersebut terjadi, dan buat satu test case spesifik yang sengaja dirancang untuk memalsukan hipotesis Anda.

### Level 2 (Menengah)
Jelaskan perbedaan antara Epistemologi Bayesian (pembaruan probabilitas kepercayaan) vs Epistemologi Popperian (falsifikasi deduktif). Kapan Bayesian lebih unggul dalam machine learning?

### Level 3 (Mahir)
Analisis batas pengetahuan komputasi: Bagaimana Teorema Ketidaklengkapan Gödel dan Halting Problem Alan Turing menetapkan batas epistemologis fundamental pada apa yang dapat diketahui oleh matematika dan komputer.
""",
        "references": """
- Popper, K. (1959). *The Logic of Scientific Discovery*. Routledge.
- Kuhn, T. S. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press.
- Chalmers, A. F. (2013). *What Is This Thing Called Science?*. Hackett Publishing.
"""
    },
    5: {
        "intuition": """
Jika komputer Anda menerima perintah: "Hapus file jika nama file berawalan A dan berakhiran .tmp, ATAU jika pengguna adalah root", bagaimana komputer yakin tidak salah menghapus file penting? 

Komputer tidak menggunakan perasaan atau intuisi; ia menggunakan **Logika Formal**. Logika formal adalah bahasa matematika murni yang mengatur validitas penarikan kesimpulan. Dalam logika formal, kebenaran suatu kesimpulan tidak ditentukan oleh apakah topik pembicaraan terdengar bagus atau masuk akal, melainkan oleh *struktur aturan inferensi* yang tidak terbantahkan.
""",
        "theory": """
### 1. Logika Proposisional & Tabel Kebenaran
Proposisi adalah pernyataan deklaratif yang bernilai Benar ($T / 1$) atau Salah ($F / 0$).
Operasi dasar:
- Negasi: $\\neg P$
- Konjungsi: $P \\land Q$
- Disjungsi: $P \\lor Q$
- Implikasi: $P \\implies Q \\equiv \\neg P \\lor Q$
- Bi-implikasi: $P \\iff Q \\equiv (P \\implies Q) \\land (Q \\implies P)$

### 2. Aturan Inferensi Deduktif Klasik
- **Modus Ponens**:
  $$\\frac{P, \\quad P \\implies Q}{\\therefore Q}$$
- **Modus Tollens**:
  $$\\frac{\\neg Q, \\quad P \\implies Q}{\\therefore \\neg P}$$

### 3. Logika Predikat & Kuantor
- Kuantor Universal: $\\forall x \\in D, P(x)$
- Kuantor Eksistensial: $\\exists x \\in D, P(x)$
- Hukum De Morgan untuk Kuantor:
  $$\\neg(\\forall x, P(x)) \\iff \\exists x, \\neg P(x)$$
  $$\\neg(\\exists x, P(x)) \\iff \\forall x, \\neg P(x)$$
""",
        "internals": """
```mermaid
graph TD
    Premis1["Premis 1: Jika server offline (P), traffic dialihkan (Q)"] --> ModusPonens{"Aturan: Modus Ponens"}
    Premis2["Premis 2: Fakta bahwa server offline (P)"] --> ModusPonens
    ModusPonens --> Kesimpulan["Kesimpulan Mutlak: Traffic PASTI dialihkan (Q)"]
```
""",
        "code_block": """```python
def check_tautology(expr_fn, var_names):
    \"\"\"
    Mengevaluasi apakah ekspresi logika proposisional adalah Tautologi (selalu bernilai True).
    \"\"\"
    n = len(var_names)
    total_assignments = 1 << n
    
    for i in range(total_assignments):
        env = {}
        for j, name in enumerate(var_names):
            env[name] = bool((i >> j) & 1)
        
        result = expr_fn(env)
        if not result:
            return False, f"Batal pada assignment: {env}"
            
    return True, f"Tautologi Valid untuk seluruh {total_assignments} kombinasi!"

# Uji Hukum De Morgan: not (P and Q) == (not P or not Q)
is_valid, msg = check_tautology(
    lambda env: (not (env['P'] and env['Q'])) == (not env['P'] or not env['Q']),
    ['P', 'Q']
)
print("Verifikasi Hukum De Morgan:")
print(f"Status: {is_valid} | Pesan: {msg}")

# Uji Implikasi: (P implies Q) == (not P or Q)
is_valid_imp, msg_imp = check_tautology(
    lambda env: ((not env['P']) or env['Q']) == (not (env['P'] and not env['Q'])),
    ['P', 'Q']
)
print("\nVerifikasi Kesetaraan Implikasi:")
print(f"Status: {is_valid_imp} | Pesan: {msg_imp}")
```""",
        "pitfalls": """
1. **Affirming the Consequent (Kekeliruan Menegaskan Akibat)**:
   - Premis: Jika hujan ($P$), jalanan basah ($Q$).
   - Fakta: Jalanan basah ($Q$).
   - Kesimpulan SALAH: Pasti hujan ($P$). (Bisa saja disiram air pemadam kebakaran!).
2. **Denying the Antecedent (Kekeliruan Menolak Sebab)**:
   - Premis: Jika hujan ($P$), jalanan basah ($Q$).
   - Fakta: Tidak hujan ($\\neg P$).
   - Kesimpulan SALAH: Jalanan pasti tidak basah ($\\neg Q$).
""",
        "exercises": """
### Level 1 (Dasar)
Buktikan menggunakan tabel kebenaran bahwa pernyataan kontrapositif $(P \\implies Q) \\iff (\\neg Q \\implies \\neg P)$ bernilai benar untuk semua kemungkinan.

### Level 2 (Menengah)
Buktikan secara formal dengan metode Kontradiksi (*Reductio ad Absurdum*) bahwa $\\sqrt{2}$ adalah bilangan irasional.

### Level 3 (Mahir)
Tulis Mini SAT Solver dalam Python (algoritma DPLL - Davis-Putnam-Logemann-Loveland) untuk menentukan satisfiability dari ekspresi Conjunctive Normal Form (CNF) 3 variabel.
""",
        "references": """
- Enderton, H. B. (2001). *A Mathematical Introduction to Logic*. Academic Press.
- Rosen, K. H. (2019). *Discrete Mathematics and Its Applications*. McGraw-Hill.
- Russell, B., & Whitehead, A. N. (1910). *Principia Mathematica*. Cambridge University Press.
"""
    }
}
