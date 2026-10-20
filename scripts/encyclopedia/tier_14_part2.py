"""Encyclopedia Tier 14 Part 2: Topics 212 - 216 (Stochastic Calculus & Black-Scholes, Financial Econometrics & GARCH/VaR, Market Microstructure & LOB, Ultra Low-Latency HFT, Blockchain Architecture & DeFi)
"""

DATA_TIER_14_PART2 = {
    212: {
        "intuition": r"""Jika Anda melempar sebutir serbuk sari ke dalam segelas air hangat, serbuk sari tersebut akan bergerak zigzag secara acak tak beraturan karena terus-menerus ditabrak oleh miliaran molekul air yang tak terlihat: inilah **Gerak Brown (Brownian Motion)** ([Einstein - Investigations on the Theory of the Brownian Movement](https://einsteinpapers.press.princeton.edu/vol2-trans/236)).

Harga saham di bursa efek bergerak persis seperti serbuk sari tersebut: ia memiliki kecenderungan melayang ke atas seiring pertumbuhan ekonomi (*drift*), tetapi di setiap detik ia dihantam oleh ribuan berita acak, rumor, dan transaksi pembeli/penjual (*volatilitas stokastik*).

Dalam kalkulus sekolah biasa, garis grafik selalu diasumsikan mulus sehingga kita bisa menghitung kemiringan turunannya. Namun grafik harga saham berliku tajam di setiap skala mikro (*nowhere differentiable*!). Matematikawan Kiyosi Itô menciptakan kalkulus baru bernama **Kalkulus Stokastik (Itô Calculus)** ([Itô - Stochastic Integral](https://www.jstor.org/stable/2371752)).

Dengan kalkulus ini, Fischer Black, Myron Scholes, dan Robert Merton memecahkan salah satu misteri terbesar peradaban finansial: **Persamaan Black-Scholes**, rumus matematika pasti untuk menentukan harga wajar kontrak opsi dengan menciptakan portofolio lindung nilai (*hedging*) yang 100% bebas risiko ([Black & Scholes - The Pricing of Options and Corporate Liabilities](https://www.jstor.org/stable/1831029)).""",
        "theory": r"""Formulasi Matematis Kalkulus Stokastik & Model Black-Scholes:

1. **Gerak Brown Geometris (Geometric Brownian Motion / GBM)**:
Model dinamika harga aset dasar $S_t$:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
Di mana $\mu$ adalah tingkat pengembalian drift, $\sigma$ volatilitas konstan, dan $W_t$ adalah proses Wiener standar dengan sifat: $W_0 = 0$, lintasan kontinu, inkremen independen $W_t - W_s \sim \mathcal{N}(0, t - s)$, dan perkalian variasional $(dW_t)^2 = dt$.

2. **Lemma Itô (Itô's Lemma 1-Dimensi)**:
Untuk fungsi mulus $V(S, t)$, ekspansi deret Taylor mempertahankan suku orde kedua $(dS)^2$ karena $(dW)^2 = dt$:
$$dV = \left( \frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \sigma S \frac{\partial V}{\partial S} dW_t$$

3. **Persamaan Diferensial Parsial (PDE) Black-Scholes**:
Membangun portofolio bebas risiko delta-neutral $\Pi = V - \Delta S$ dengan memilih rasio lindung nilai $\Delta = \frac{\partial V}{\partial S}$. Menurut prinsip arbitrase, imbal hasil portofolio harus sama dengan suku bunga bebas risiko ($d\Pi = r \Pi dt$):
$$\frac{\partial V}{\partial t} + r S \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - r V = 0$$

4. **Solusi Analitik Opsi Call Eropa & Parameter Sensitivitas (The Greeks)**:
$$C(S, t) = S_0 N(d_1) - K e^{-r(T-t)} N(d_2)$$
$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)(T-t)}{\sigma \sqrt{T-t}}, \quad d_2 = d_1 - \sigma \sqrt{T-t}$$
* **Delta ($\Delta$)**: $\frac{\partial C}{\partial S} = N(d_1)$ (Sensitivitas harga terhadap pergerakan aset dasar)
* **Gamma ($\Gamma$)**: $\frac{\partial^2 C}{\partial S^2} = \frac{N'(d_1)}{S \sigma \sqrt{T-t}}$ (Tingkat perubahan delta)
* **Vega ($\nu$)**: $\frac{\partial C}{\partial \sigma} = S \sqrt{T-t} N'(d_1)$ (Sensitivitas terhadap volatilitas pasar)
* **Theta ($\Theta$)**: $\frac{\partial C}{\partial t}$ (Peluruhan nilai waktu harian / *time decay*)
* **Rho ($\rho$)**: $\frac{\partial C}{\partial r} = K (T-t) e^{-r(T-t)} N(d_2)$ (Sensitivitas terhadap suku bunga).""",
        "internals": r"""Arsitektur mekanisme Delta Hedging dinamis untuk menetralisir risiko portofolio opsi:

```mermaid
flowchart TD
    Market["Harga Saham S_t Berfluktuasi"] --> CalcDelta["Hitung Delta Opsi Real-Time: Delta = N(d_1)"]
    CalcDelta --> Portfolio["Portofolio Hedged: Pi = Long 1 Call - Delta Lembar Saham"]
    Portfolio --> Rebalance["Rebalancing Siklus: Jika Delta Berubah, Beli/Jual Saham Penyeimbang"]
    Rebalance --> RiskNeutral["Portofolio Kebal terhadap Pergerakan Arah Pasar (Delta-Neutral)"]
    RiskNeutral -.->|"Keuntungan Murni Berasal dari Peluruhan Nilai Waktu (Theta vs Gamma)"| PnL["Stabilitas PnL"]
```

Dengan menjaga posisi selalu *Delta-Neutral* ($\sum \Delta = 0$), pedagang opsi tidak peduli apakah harga saham naik atau turun; mereka murni memperdagangkan selisih antara volatilitas tersirat pasar (*Implied Volatility*) dengan volatilitas riil aset (*Realized Volatility*) ([Hull Derivatives Book Chapter 19](https://www.pearson.com/en-us/subject-catalog/p/options-futures-and-other-derivatives/P200000003339)).""",
        "code_block": r"""```python
import numpy as np
from scipy.stats import norm

# 1. Penetapan Harga Opsi Call & Put Eropa Black-Scholes Analitik
def black_scholes_pricing(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    # Hitung The Greeks
    delta_call = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * np.sqrt(T) * norm.pdf(d1) / 100 # per 1% vol shift
    theta_call = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    
    return {
        "call_price": call_price, "put_price": put_price,
        "delta": delta_call, "gamma": gamma, "vega": vega, "theta": theta_call
    }

# 2. Simulasi Monte Carlo Gerak Brown Geometris (GBM)
def simulate_gbm(S0, mu, sigma, T, steps, paths):
    dt = T / steps
    # dS = S * (mu*dt + sigma*sqrt(dt)*Z)
    Z = np.random.normal(0, 1, size=(steps, paths))
    log_returns = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    price_paths = np.vstack([np.full(paths, S0), S0 * np.exp(np.cumsum(log_returns, axis=0))])
    return price_paths

# Parameter Pasar
S0 = 100.0   # Harga Saham Awal
K = 105.0    # Strike Price
T = 0.5      # 6 Bulan (0.5 Tahun)
r = 0.05     # 5% Risk-free rate
sigma = 0.25 # 25% Volatilitas Tahunan

res = black_scholes_pricing(S0, K, T, r, sigma)
print(f"Harga Call Opsi BS   : ${res['call_price']:.2f}")
print(f"Harga Put Opsi BS    : ${res['put_price']:.2f}")
print(f"Delta (Rasio Lindung): {res['delta']:.4f}")
print(f"Gamma                : {res['gamma']:.4f}")
print(f"Vega (per 1% Vol)    : ${res['vega']:.3f}")
print(f"Theta (per Hari)     : ${res['theta']:.3f}")

# Validasi Monte Carlo terhadap Harga Analitik
np.random.seed(42)
sim_paths = simulate_gbm(S0, r, sigma, T, steps=252, paths=100_000)
final_prices = sim_paths[-1]
mc_payoffs = np.maximum(final_prices - K, 0)
mc_call = np.exp(-r * T) * np.mean(mc_payoffs)
print(f"Harga Call Monte Carlo (100k paths): ${mc_call:.2f} (Konvergen sempurna!)")
```""",
        "pitfalls": r"""*The Volatility Smile & Ekor Gemuk (Fat-Tail Breakdown)*: Model Black-Scholes murni mengasumsikan volatilitas konstan $\sigma$ dan distribusi log-return normal murni. Di pasar finansial nyata sejak Black Monday 1987, pasar mengalami *volatility smile/skew* (opsi deep out-of-the-money memiliki implied volatility yang jauh lebih tinggi karena pasar memperhitungkan risiko kejatuhan pasar ekstrem / *fat tails*). Menggunakan Black-Scholes tanpa kalibrasi kurva *local volatility Dupire* atau model stokastik *Heston* akan menyebabkan kerugian besar saat terjadi krisis pasar ([Derman & Kani - The Volatility Smile](https://www.ederman.com/wp-content/uploads/1994/01/the_volatility_smile.pdf)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis solver pencarian *Implied Volatility* opsi menggunakan metode biseksi: terima harga pasar observasi opsi call, harga saham, strike, dan tenor, lalu temukan nilai parameter $\sigma$ Black-Scholes yang menyamakan harga analitik dengan harga pasar hingga toleransi $10^{-4}$.
*Rubrik*: Solver konvergen dalam kurang dari 20 iterasi.

### Level 2 (Menengah)
Bangun simulator strategi *Dynamic Delta Hedging*: simulasikan 100 jalur lintasan harga GBM harian selama 1 tahun untuk posisi Short 100 Kontrak Call Opsi, lakukan penyesuaian posisi saham (*rebalancing*) setiap hari untuk menjaga portofolio tetap delta-neutral, dan hitung distribusi PnL akhir di hadapan biaya transaksi komisi broker.
*Rubrik*: Menghasilkan visualisasi PnL tracking error terhadap frekuensi rebalancing.

### Level 3 (Mahir)
Implementasikan algoritma kisi binomial Cox-Ross-Rubinstein (CRR Binomial Tree) untuk opsi Amerika (*American Put Option* yang dapat dieksekusi lebih awal sebelum maturitas / *early exercise*):
$$u = e^{\sigma \sqrt{\Delta t}}, \quad d = \frac{1}{u}, \quad p = \frac{e^{r \Delta t} - d}{u - d}$$
Bandingkan harga opsi Put Amerika terhadap opsi Put Eropa, dan buktikan batas early exercise premium yang selalu positif.
*Rubrik*: Tree rekursif dengan 500 langkah waktu memvalidasi harga opsi Amerika secara numerik.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Pricing of Options and Corporate Liabilities | Fischer Black & Myron Scholes | [Journal of Political Economy 1973](https://www.jstor.org/stable/1831029) | Makalah Hadiah Nobel Penemuan Rumus Black-Scholes |
| Stochastic Differential Equations (6th Ed.) | Bernt Øksendal | [Springer Universitext](https://link.springer.com/book/10.1007/978-3-642-14394-6) | Pembuktian Matematis Ketat Itô Calculus & Integral Martingale |
| Dynamic Hedging: Managing Vanilla and Exotic Options | Nassim Nicholas Taleb | [Wiley Finance Portal](https://www.wiley.com/en-us/Dynamic+Hedging%3A+Managing+Vanilla+and+Exotic+Options-p-9780471152804) | Praktik Industri Perdagangan Opsi, The Greeks, Volatility Trading |
| Continuous-Time Finance | Robert C. Merton (Nobel Laureate) | [Blackwell Publishers](https://www.wiley.com/en-us/Continuous+Time+Finance-p-9780631185086) | Generalisasi Model Arbitrase Merton, Jump Diffusion Models |"""
    },
    213: {
        "intuition": r"""Bayangkan Anda melihat grafik cuaca laut. Ada hari-hari di mana ombak laut sangat tenang selama berminggu-minggu, lalu tiba-tiba badai topan datang: ombak raksasa setinggi 10 meter mengamuk selama tiga hari berturut-turut sebelum mereda kembali.

Pasar finansial berperilaku persis seperti cuaca laut tersebut: ia memiliki sifat **Pengelompokan Volatilitas (Volatility Clustering)** ([Mandelbrot - The Variation of Certain Speculative Prices](https://www.jstor.org/stable/2350970)). Hari di mana harga saham berguncang dahsyat kemungkinan besar akan diikuti oleh hari-hari yang berguncang dahsyat pula besoknya; dan hari yang tenang cenderung diikuti oleh hari yang tenang.

Model statistik biasa yang mengasumsikan varians konstan (*homoskedastisitas*) akan buta terhadap fenomena ini. Robert Engle menemukan model **GARCH (Generalized Autoregressive Conditional Heteroskedasticity)** untuk meramalkan badai volatilitas pasar esok hari ([Engle - Nobel Lecture 2003](https://www.nobelprize.org/prizes/economic-sciences/2003/engle/lecture/)).

Selain itu, bagaimana sebuah institusi keuangan raksasa (seperti bank sentral atau dana pensiun) mengetahui seberapa besar uang yang bisa hilang dalam satu hari terburuk? Mereka menggunakan **Value at Risk (VaR)**: ukuran risiko standar yang memberi tahu dewan direksi: *"Kami 99% yakin bahwa kerugian portofolio kami besok tidak akan melebihi Rp 50 miliar"* ([Jorion - Value at Risk: The New Benchmark for Managing Financial Risk](https://www.mheducation.com/highered/product/value-risk-new-benchmark-managing-financial-risk-jorion/M9780071464956.html)).""",
        "theory": r"""Formulasi Ekonometrika Deret Waktu Finansial & Risiko:

1. **Model Volatilitas Dinamis GARCH$(p, q)$ (Bollerslev 1986)**:
Untuk return terpusat $\epsilon_t = \sigma_t z_t$ dengan derau putih standar $z_t \sim \text{i.i.d.}(0, 1)$:
Varians bersyarat $\sigma_t^2$ bergantung pada kuadrat galat masa lalu (suku ARCH $q$) dan varians masa lalu (suku GARCH $p$):
$$\sigma_t^2 = \omega + \sum_{i=1}^q \alpha_i \epsilon_{t-i}^2 + \sum_{j=1}^p \beta_j \sigma_{t-j}^2$$
Syarat stasionaritas kovarians ketat: $\omega > 0, \alpha_i \ge 0, \beta_j \ge 0$, dan $\sum_{i=1}^q \alpha_i + \sum_{j=1}^p \beta_j < 1$.
Volatilitas jangka panjang tanpa syarat (*unconditional variance*): $\sigma_L^2 = \frac{\omega}{1 - \sum \alpha_i - \sum \beta_j}$ ([Bollerslev - Generalized Autoregressive Conditional Heteroskedasticity](https://www.sciencedirect.com/science/article/pii/0304407686900631)).

2. **Kointegrasi & Pasangan Perdagangan Statistik (Engle-Granger Two-Step)**:
Dua deret waktu non-stasioner $X_t, Y_t \sim I(1)$ berkointegrasi jika terdapat kombinasi linier stasioner $\epsilon_t \sim I(0)$:
$$Y_t = \beta X_t + \alpha + \epsilon_t, \quad \Delta \epsilon_t = \gamma \epsilon_{t-1} + u_t$$
Jika uji Augmented Dickey-Fuller (ADF) pada residual $\epsilon_t$ menolak hipotesis nol akar unit ($p < 0.05$), hubungan *mean-reverting* jangka panjang terbukti, menjadi landasan strategi arbitrase statistik pasangan saham (*Pairs Trading*) ([Engle & Granger - Co-integration and Error Correction](https://www.jstor.org/stable/1913236)).

3. **Value at Risk (VaR) & Expected Shortfall (CVaR)**:
* Parametrik Gaussian VaR pada tingkat kepercayaan $\alpha$ (misal 99%) untuk horizon waktu $h$:
$$\text{VaR}_\alpha = - (\mu \cdot h + z_\alpha \cdot \sigma \sqrt{h}) \cdot \text{Portfolio Value}$$
* Expected Shortfall / Conditional VaR (Koheren menurut aksioma Artzner): Rata-rata kerugian pada ekor distribusi ketika VaR telah terlampaui:
$$\text{ES}_\alpha = \mathbb{E}\left[ L \mid L > \text{VaR}_\alpha \right] = \frac{1}{1 - \alpha} \int_\alpha^1 \text{VaR}_u du$$""",
        "internals": r"""Arsitektur pipeline backtesting dan pelaporan risiko harian institusi finansial (Basel III Traffic Light System):

```mermaid
flowchart TD
    Historical["Data Historis Return Portofolio 500 Hari"] --> Engine["Mesin Kalkulasi Risiko Harian"]
    Engine --> Parametric["Metode 1: Parametrik GARCH-VaR"]
    Engine --> HistoricalSim["Metode 2: Simulasi Historis Non-Parametrik"]
    Engine --> MonteCarlo["Metode 3: Simulasi Monte Carlo Multi-Faktor"]
    
    Parametric & HistoricalSim & MonteCarlo --> VaR99["Laporan VaR 99% Harian: Maksimum Rugi Rp 50 Miliar"]
    VaR99 --> Backtest["Uji Validasi Backtesting Kupiec POF Test"]
    Backtest --> Basel["Basel Regulatory Zones: Hijau (<4 exceptions), Kuning, Merah"]
```

Uji Backtesting Kupiec Likelihood Ratio (POF Test) memverifikasi apakah jumlah pelanggaran aktual (*exceptions* di mana kerugian riil melebihi estimasi VaR) sesuai dengan ekspektasi probabilitas $1 - \alpha$, mencegah bank meremehkan cadangan modal risiko ([Kupiec - Techniques for Verifying the Accuracy of Risk Measurement Models](https://www.sciencedirect.com/science/article/pii/1057819695000049)).""",
        "code_block": r"""```python
import numpy as np
from scipy import stats

# 1. Simulasi Model Volatilitas Dinamis GARCH(1,1)
def simulate_garch11(n=1000, omega=0.00001, alpha=0.1, beta=0.85):
    # Syarat stasionaritas: alpha + beta < 1 (0.1 + 0.85 = 0.95 < 1)
    returns = np.zeros(n)
    sigma2 = np.zeros(n)
    sigma2[0] = omega / (1.0 - alpha - beta) # Varians tanpa syarat awal
    
    z = np.random.normal(0, 1, n)
    for t in range(1, n):
        # sigma_t^2 = omega + alpha * eps_{t-1}^2 + beta * sigma_{t-1}^2
        sigma2[t] = omega + alpha * (returns[t-1]**2) + beta * sigma2[t-1]
        returns[t] = np.sqrt(sigma2[t]) * z[t]
        
    return returns, np.sqrt(sigma2)

# 2. Perhitungan Value at Risk (VaR) & Expected Shortfall (CVaR)
def calculate_risk_metrics(returns, confidence_level=0.99, portfolio_value=1_000_000_000):
    # Metode Simulasi Historis (Non-Parametrik)
    cutoff_percentile = (1.0 - confidence_level) * 100
    var_return = np.percentile(returns, cutoff_percentile)
    var_amount = -var_return * portfolio_value
    
    # Expected Shortfall (Rata-rata kerugian di luar batas VaR)
    tail_losses = returns[returns <= var_return]
    cvar_return = np.mean(tail_losses)
    cvar_amount = -cvar_return * portfolio_value
    
    return var_amount, cvar_amount

np.random.seed(42)
sim_returns, sim_vol = simulate_garch11(n=2500)
var_99, cvar_99 = calculate_risk_metrics(sim_returns, confidence_level=0.99, portfolio_value=100_000_000)

print(f"Portofolio Modal Dasar: Rp 100,000,000")
print(f"Value at Risk 99% 1-Hari (Historical) : Rp {var_99:,.2f}")
print(f"Expected Shortfall 99% (CVaR)         : Rp {cvar_99:,.2f} (Ekor kerugian rata-rata)")
print(f"Volatilitas GARCH Rata-rata Terestrimasi: {np.mean(sim_vol)*100*np.sqrt(252):.2f}% tahunan")
```""",
        "pitfalls": r"""*Kegagalan Sub-Additivitas pada Value at Risk (VaR Non-Coherence)*: Secara matematika, VaR tidak memenuhi aksioma sub-additivitas Artzner ($\text{VaR}(A + B) \le \text{VaR}(A) + \text{VaR}(B)$ tidak selalu terpenuhi pada distribusi ekor gemuk non-normal). Artinya, menggabungkan dua portofolio dapat menghasilkan angka VaR gabungan yang tampak *lebih besar* daripada penjumlahan risiko masing-masing portofolio, mematikan insentif diversifikasi. Inilah alasan Komite Basel secara resmi beralih dari VaR ke **Expected Shortfall (ES)** dalam regulasi Fundamental Review of the Trading Book (FRTB) ([Artzner et al. - Coherent Measures of Risk](https://link.springer.com/article/10.1007/s007800050068)).""",
        "exercises": r"""### Level 1 (Pemula)
Gunakan modul `arch` di Python (`arch.arch_model`) untuk melatih model GARCH(1,1) pada deret waktu return harian saham publik nyata atau sintetis, laporkan estimasi koefisien $(\omega, \alpha, \beta)$, dan periksa apakah nilai p-value signifikan secara statistik.
*Rubrik*: Output mencetak tabel ringkasan estimasi Maximum Likelihood model GARCH.

### Level 2 (Menengah)
Bangun strategi perdagangan pasangan saham (*Pairs Trading*) berbasis Uji Kointegrasi dua tahap Engle-Granger di Python: estimasikan koefisien lindung nilai $\beta$ via OLS, hitung deret residual spread $\epsilon_t = Y_t - \beta X_t$, hitung skor z-score bergulir $\frac{\epsilon_t - \mu}{\sigma}$, dan buat aturan sinyal buka posisi beli/jual saat $|z| > 2.0$ serta tutup posisi saat $z \to 0$.
*Rubrik*: Strategi mengeksekusi perdagangan mean-reversion pada spread terkointegrasi.

### Level 3 (Mahir)
Implementasikan uji backtesting independen **Kupiec Proportion of Failures (POF)** dan **Christoffersen Independence Test** dari awal: terima deret waktu return portofolio riil 1.000 hari dan estimasi VaR 99% harian, catat urutan pelanggaran biner $I_t \in \{0, 1\}$, hitung rasio likelihood $\text{LR}_{\text{POF}}$ dan $\text{LR}_{\text{ind}}$, serta tentukan apakah model VaR lolos uji independensi bersyarat pada tingkat signifikansi $5\%$.
*Rubrik*: Formulasi rasio likelihood chi-square terhitung tepat sesuai formula Kupiec.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Generalized Autoregressive Conditional Heteroskedasticity (GARCH) | Tim Bollerslev | [Journal of Econometrics 1986](https://www.sciencedirect.com/science/article/pii/0304407686900631) | Formulasi Asli Teori GARCH dan Pemodelan Volatilitas |
| Co-integration and Error Correction: Representation, Estimation, and Testing | Robert F. Engle & Clive W. J. Granger (Nobel 2003) | [Econometrica 1987](https://www.jstor.org/stable/1913236) | Teori Asli Kointegrasi Pasangan Deret Waktu Finansial |
| Value at Risk: The New Benchmark for Managing Financial Risk (3rd Ed.) | Philippe Jorion (UC Irvine) | [McGraw-Hill Professional](https://www.mheducation.com/highered/product/value-risk-new-benchmark-managing-financial-risk-jorion/M9780071464956.html) | Alkitab Manajemen Risiko Pasar, Parametrik vs Monte Carlo VaR |
| Coherent Measures of Risk | Philippe Artzner, Freddy Delbaen, Jean-Marc Eber, David Heath | [Mathematical Finance 1999](https://link.springer.com/article/10.1007/s007800050068) | Aksioma Koherensi Risiko Finansial, Expected Shortfall (CVaR) |"""
    },
    214: {
        "intuition": r"""Jika Anda pergi ke pasar tradisional, ada penjual yang meneriakkan: *"Saya jual apel ini seharga Rp 10.000!"*, dan ada pembeli yang menawar: *"Saya mau beli apelmu kalau harganya Rp 8.000!"*. Transaksi baru terjadi jika salah satu pihak mengalah dan menyepakati harga di tengah.

Di bursa efek modern (seperti Nasdaq, NYSE, atau Bursa Efek Indonesia), tidak ada teriakan manusia di lantai bursa lagi. Seluruh aktivitas perdagangan ditangani oleh komputer pencocok pesan berkecepatan mikrodetik bernama **Mesin Pencocok Pesan (Matching Engine)** yang mengelola antrean raksasa bernama **Buku Pesanan Terbatas (Limit Order Book / LOB)** ([Harris - Trading and Exchanges: Market Microstructure for Practitioners](https://academic.oup.com/book/52486)).

Buku pesanan memiliki dua sisi:
1. **Sisi Beli (Bids)**: Daftar antrean orang-orang yang ingin membeli, diurutkan dari harga penawaran tertinggi ke terendah.
2. **Sisi Jual (Asks)**: Daftar antrean orang-orang yang ingin menjual, diurutkan dari harga permintaan terendah ke tertinggi.

Selisih antara harga jual termurah dan harga beli termahal disebut **Bid-Ask Spread**. Dan bagaimana dana institusi besar (seperti BlackRock) membeli saham senilai triliunan rupiah tanpa membuat harga pasar meroket liar? Mereka menggunakan algoritma eksekusi bertahap seperti **Time-Weighted Average Price (TWAP)** dan **Volume-Weighted Average Price (VWAP)** ([Almgren & Chriss - Optimal Execution of Portfolio Transactions](https://www.sciencedirect.com/science/article/pii/S1057819600000072)).""",
        "theory": r"""Formulasi Matematis Mikrostruktur Pasar & Buku Pesanan:

1. **Struktur Formal Limit Order Book (LOB)**:
Buku pesanan pada waktu $t$ didefinisikan sebagai dua himpunan harga dan kuantitas terurut:
$$\mathcal{B}_t = \{(p_i^b, q_i^b)\}_{i=1}^{N_b}, \quad p_1^b > p_2^b > \dots > p_{N_b}^b \quad (\text{Best Bid } p_1^b)$$
$$\mathcal{A}_t = \{(p_j^a, q_j^a)\}_{j=1}^{N_a}, \quad p_1^a < p_2^a < \dots < p_{N_a}^a \quad (\text{Best Ask } p_1^a)$$
Invarian pasar bebas arbitrase: $p_1^b < p_1^a$.
* Bid-Ask Spread: $S_t = p_1^a - p_1^b > 0$
* Mid-Price: $M_t = \frac{p_1^a + p_1^b}{2}$
* Micro-Price (Memperhitungkan ketidakseimbangan volume / *Order Book Imbalance*):
$$P_{\text{micro}} = \frac{q_1^b p_1^a + q_1^a p_1^b}{q_1^b + q_1^a} = M_t + \frac{S_t}{2} \left( \frac{q_1^b - q_1^a}{q_1^b + q_1^a} \right)$$

2. **Prioritas Pencocokan Pesanan (Price-Time Priority / FIFO)**:
Mesin pencocok pesanan mengeksekusi pesanan pasar (*Market Order*) terhadap pesanan terbatas (*Limit Order*) teratas berdasarkan:
1. Prioritas Harga Terbaik (Harga jual lebih murah atau beli lebih mahal didahulukan).
2. Prioritas Waktu Kedatangan (Pada tingkat harga yang identik, pesanan yang tiba lebih awal dieksekusi terlebih dahulu).

3. **Model Dampak Pasar Almgren-Chriss (Optimal Execution)**:
Membagi eksekusi order besar $X$ ke dalam $N$ interval waktu $t_k$:
Biaya dampak pasar permanen linier $\gamma$ dan dampak temporer $\eta$:
$$\min_{\tau} \mathbb{E}[x^T \Lambda x] + \lambda \mathbb{V}\text{ar}[x^T \Lambda x]$$
Strategi eksekusi TWAP statis memecah pesanan secara merata $v_k = \frac{X}{N}$ di sepanjang durasi hari bursa untuk meminimalkan jejak kaki pasar ([Almgren & Chriss 2000](https://www.sciencedirect.com/science/article/pii/S1057819600000072)).""",
        "internals": r"""Arsitektur struktur data berperforma tinggi Limit Order Book dalam C++ (Double-Linked List + Hash Map):

```mermaid
flowchart TD
    subgraph Price_Tree["Price Index (Red-Black Tree / Array Monotonik O(1))"]
        P101["Harga Ask: $101.00"]
        P100["Harga Bid: $100.50 (Best Bid)"]
        P99["Harga Bid: $100.00"]
    end
    subgraph Queue_100["FIFO Double-Linked List pada Tingkat Harga $100.50"]
        O1["Order #1001 (Vol: 50 lot)"]
        O2["Order #1002 (Vol: 120 lot)"]
        O3["Order #1003 (Vol: 30 lot)"]
        O1 <--> O2 <--> O3
    end
    P100 --> Queue_100
    subgraph Lookup_Map["Order Map: ID -> Pointer (O(1) Cancellation)"]
        Map["HashMap: 1002 -> &OrderNode"]
    end
    Map -.-> O2
```

Dengan arsitektur *Double-Linked List* per tingkat harga dan *Hash Table* pointer pesanan, operasi pembatalan pesanan (*Cancel Order*) dan eksekusi pencocokan (*Fill Order*) dapat diselesaikan dalam kompleksitas waktu konstan murni $\mathcal{O}(1)$ tanpa pencarian linier ([O'Hara - Market Microstructure Theory](https://www.wiley.com/en-us/Market+Microstructure+Theory-p-9780631207610)).""",
        "code_block": r"""```python
from collections import deque
from dataclasses import dataclass

# 1. Implementasi Sederhana Mesin Pencocok Pesanan (Matching Engine FIFO)
@dataclass
class Order:
    order_id: int
    side: str # 'BUY' atau 'SELL'
    price: float
    qty: int

class OrderBook:
    def __init__(self):
        self.bids = {} # price -> deque([Order, ...])
        self.asks = {} # price -> deque([Order, ...])
        
    def add_limit_order(self, order: Order):
        book = self.bids if order.side == 'BUY' else self.asks
        if order.price not in book:
            book[order.price] = deque()
        book[order.price].append(order)
        
    def match_market_order(self, side: str, qty: int):
        # Market order beli mencocokkan ask terendah; market order jual mencocokkan bid tertinggi
        filled_trades = []
        remaining_qty = qty
        
        while remaining_qty > 0:
            if side == 'BUY':
                if not self.asks:
                    break # Buku Ask Kosong
                best_price = min(self.asks.keys())
                queue = self.asks[best_price]
            else:
                if not self.bids:
                    break # Buku Bid Kosong
                best_price = max(self.bids.keys())
                queue = self.bids[best_price]
                
            top_order = queue[0]
            trade_qty = min(remaining_qty, top_order.qty)
            
            filled_trades.append((top_order.order_id, best_price, trade_qty))
            top_order.qty -= trade_qty
            remaining_qty -= trade_qty
            
            if top_order.qty == 0:
                queue.popleft()
                if not queue:
                    del (self.asks if side == 'BUY' else self.bids)[best_price]
                    
        return filled_trades, remaining_qty

# Uji Coba Buku Pesanan
lob = OrderBook()
lob.add_limit_order(Order(101, 'SELL', 100.5, 50))  # Ask 1
lob.add_limit_order(Order(102, 'SELL', 100.5, 100)) # Ask 2 (Antrean sama)
lob.add_limit_order(Order(103, 'SELL', 101.0, 200)) # Ask 3 (Harga lebih tinggi)

# Eksekusi Market Order Beli 80 Lot
trades, unfulfilled = lob.match_market_order('BUY', 80)
print("Transaksi Berhasil Dieksekusi:")
for t in trades:
    print(f" - Terisi terhadap Order #{t[0]} di Harga ${t[1]:.2f} sebanyak {t[2]} lot")
print(f"Sisa Kuota Belum Terisi: {unfulfilled} lot")
```""",
        "pitfalls": r"""*Adverse Selection & Latency Arbitrage pada Limit Order*: Menempatkan pesanan limit pasif di buku pesanan seperti meninggalkan penawaran terbuka yang bisa dieksploitasi oleh pedagang frekuensi tinggi (HFT) yang lebih cepat. Jika berita makro ekonomi keluar dan harga pasar global anjlok, algoritma HFT akan mengeksekusi (*sniping*) pesanan beli limit Anda sebelum komputer Anda sempat mengirim instruksi pembatalan (*cancel request*), meninggalkan Anda dengan posisi rugi instan ([Budish, Cramton, Shim - The High-Frequency Trading Arms Race](https://academic.oup.com/qje/article/130/4/1547/1916146)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis modul kalkulasi metrik buku pesanan: terima snapshot kedalaman pasar (Depth of Market 5 tingkat), hitung nilai Mid-Price, Micro-Price berbobot volume, dan Order Book Imbalance rasio $\text{OBI} = \frac{Q_{\text{bid}} - Q_{\text{ask}}}{Q_{\text{bid}} + Q_{\text{ask}}}$.
*Rubrik*: Output mencetak metrik mikrostruktur dengan benar.

### Level 2 (Menengah)
Bangun simulator eksekusi algoritma Time-Weighted Average Price (TWAP): bagi order induk 10.000 lot saham menjadi 20 sub-order anak yang dikirimkan secara berkala setiap 5 menit, jalankan terhadap simulasi buku pesanan dinamis, dan hitung nilai slippage terhadap rata-rata harga pasar harian.
*Rubrik*: Algoritma mengeksekusi seluruh kuota tanpa melanggar batasan interval waktu.

### Level 3 (Mahir)
Implementasikan mesin pencocok pesanan Limit Order Book (LOB) performa tinggi di C++ atau Python berorientasi pointer: gunakan representasi struktur data ganda `std::map<Price, LimitLevel>` untuk pohon harga dan intrusive doubly-linked list untuk antrean FIFO pesanan, buktikan bahwa operasi `cancel_order` dan `insert_limit` dieksekusi dalam kompleksitas waktu rata-rata $\mathcal{O}(1)$.
*Rubrik*: Benchmark performa mampu memproses minimal 500.000 pesan order per detik.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Trading and Exchanges: Market Microstructure for Practitioners | Larry Harris (USC Marshall / Chief Economist SEC) | [Oxford University Press](https://academic.oup.com/book/52486) | Alkitab Mikrostruktur Pasar, LOB, Market Makers, Liquidity |
| Optimal Execution of Portfolio Transactions | Robert Almgren & Neil Chriss | [Journal of Risk 2000 Paper](https://www.sciencedirect.com/science/article/pii/S1057819600000072) | Model Matematis Dampak Pasar TWAP, VWAP, Optimal Slicing |
| The High-Frequency Trading Arms Race: Frequent Batch Auctions | Eric Budish, Peter Cramton, John Shim | [The Quarterly Journal of Economics](https://academic.oup.com/qje/article/130/4/1547/1916146) | Analisis Latency Arbitrage, Masalah Continuous-Time Books |
| Market Microstructure Theory | Maureen O'Hara (Cornell University) | [Wiley-Blackwell Classic](https://www.wiley.com/en-us/Market+Microstructure+Theory-p-9780631207610) | Teori Informasi Asimetris, Model Glosten-Milgrom & Kyle |"""
    },
    215: {
        "intuition": r"""Bagi manusia, satu kedipan mata membutuhkan waktu sekitar 300 milidetik (300.000 mikrodetik). Bagi sebuah sistem perdagangan frekuensi tinggi (**High-Frequency Trading / HFT**), 300 milidetik adalah keabadian yang sangat lambat!

Dalam arena HFT modern, pertarungan kecepatan diukur dalam hitungan **Nanodetik ($10^{-9}\text{ detik}$)**. Satu nanodetik adalah waktu yang dibutuhkan cahaya untuk merambat sepanjang 30 sentimeter di udara ([Lewis - Flash Boys: A Wall Street Revolt](https://wwnorton.com/books/Flash-Boys/)).

Jika server Anda membutuhkan waktu 10 mikrodetik untuk membaca paket data harga dari bursa dan memutuskan untuk membeli, kompetitor yang servernya membutuhkan 9 mikrodetik akan selalu mendahului Anda, merebut keuntungan, dan membuat strategi Anda rugi total.

Untuk mencapai latensi ultra-rendah:
1. **Zero-Allocation**: Memori tidak boleh dialokasikan selama jam perdagangan (*no dynamic malloc/new*) untuk menghindari penundaan siklus OS.
2. **Kernel-Bypass (DPDK / Solarflare OpenOnload)**: Kartu jaringan (NIC) menyalin paket data langsung ke memori aplikasi di ruang pengguna (*User Space*), melewati sistem operasi Linux sepenuhnya ([DPDK - Data Plane Development Kit](https://www.dpdk.org/)).
3. **Hardware Acceleration (FPGA)**: Logika pengambilan keputusan dibakar langsung ke dalam gerbang silikon chip FPGA, mengeksekusi logika strategi dalam waktu kurang dari 50 nanodetik (*Tick-to-Trade*) ([Dehmamy et al. - Ultra-Low Latency FPGA Trading](https://ieeexplore.ieee.org/document/8445123)).""",
        "theory": r"""Formulasi Rekayasa Latensi Deterministik & Teori Antrean:

1. **Hukum Little dalam Teori Antrean Sistem Trading**:
Hubungan antara jumlah pesanan dalam sistem antrean $L$, tingkat kedatangan pesanan per detik $\lambda$, dan waktu tunggu latensi rata-rata $W$:
$$L = \lambda W \implies W = \frac{L}{\lambda}$$
Pada beban lalu lintas tinggi (*high packet burst*), variabilitas latensi melonjak eksponensial mengikuti distribusi M/M/1 atau M/G/1:
$$W_q = \frac{\rho}{1 - \rho} \frac{1}{\mu}, \quad \rho = \frac{\lambda}{\mu} \to 1 \implies W_q \to \infty$$
Rekayasa HFT berfokus pada pemangkasan ekor persentil ke-99.99 (*tail latency*) agar tetap deterministik di bawah 1 mikrodetik.

2. **Antrean Bebas-Kunci Produsen Tunggal Konsumen Tunggal (Lock-Free SPSC Ring Buffer)**:
Dua thread berjalan paralel tanpa mutex/kondisi kunci (*lock-free*), hanya mengandalkan operasi instruksi atomik CPU dengan semantik sinkronisasi memori `std::memory_order_acquire` dan `std::memory_order_release` ([Leslie Lamport - Concurrent Reading and Writing](https://dl.acm.org/doi/10.1145/359642.359659)):
$$\text{Head} \leftarrow (\text{Head} + 1) \pmod N, \quad \text{Tail} \leftarrow (\text{Tail} + 1) \pmod N$$
Ukuran buffer $N$ selalu dipilih berupa bilangan pangkat dua ($N = 2^k$) sehingga operasi modulo digantikan oleh operasi bitwise kencang: `idx = count & (N - 1)`.

3. **Penghindaran False Sharing pada Garis Cache CPU (Cache Line Alignment)**:
Satu garis cache prosesor x86 modern berukuran tepat 64 bytes. Jika variabel `head` dan `tail` yang dimodifikasi oleh dua inti CPU berbeda berada pada garis cache 64-byte yang sama, protokol koherensi cache (MESI) akan terus-menerus membatalkan cache lokal (*cache ping-pong*), menghancurkan performa hingga ratusan siklus clock. Variabel harus dipisahkan oleh padding: `alignas(64)`.

4. **Metrik Tick-to-Trade Hardware FPGA**:
$$\text{Latency}_{\text{T2T}} = t_{\text{Egress Packet Out}} - t_{\text{Ingress Packet In}} < 100\text{ ns}$$""",
        "internals": r"""Arsitektur sistem HFT Kernel-Bypass DPDK vs Jaringan Linux Konvensional:

```mermaid
flowchart TD
    subgraph Traditional_OS["Linux Kernel Network Stack (Lambat: ~10 - 25 us)"]
        NIC1["Physical NIC"] --> IRQ["Hardware Interrupt (CPU Preemption)"]
        IRQ --> KernelSpace["Linux Kernel sk_buff Ring Buffer"]
        KernelSpace --> Syscall["Syscall Context Switch: recv()"]
        Syscall --> App1["Aplikasi User-Space (Salinan Memori Tambahan)"]
    end
    subgraph Kernel_Bypass["Kernel-Bypass Architecture (Ultra-Fast: < 1 us)"]
        NIC2["Physical NIC (Solarflare / Mellanox)"] --> DMA["Direct Memory Access (DMA via DPDK)"]
        DMA --> UserMem["HugePages User Memory Ring Buffer (Zero-Copy)"]
        UserMem --> PollingLoop["Dedicated Pinned Core 100% Polling Loop"]
        PollingLoop --> App2["Trading Strategy Core Engine"]
    end
```

Dengan mengeliminasi interupsi kernel perangkat keras, peralihan konteks (*context switch*), dan penyalinan memori buffer, Kernel-Bypass memangkas latensi jaringan sebesar $90\%$ dan menjaga latensi tetap deterministik (*jitter-free*) ([DPDK Documentation](https://www.dpdk.org/)).""",
        "code_block": r"""```cpp
// Konsep Desain Buffer C++ Bebas Kunci SPSC (Single-Producer Single-Consumer) Berlatensi Rendah
#include <atomic>
#include <cstdint>
#include <new>

template <typename T, size_t Capacity>
class LockFreeSPSCQueue {
    static_assert((Capacity & (Capacity - 1)) == 0, "Kapasitas harus berupa pangkat dua (2^n)!");
public:
    LockFreeSPSCQueue() : head_(0), tail_(0) {}

    // Produsen (Hanya dipanggil oleh Producer Thread)
    bool push(const T& item) {
        const size_t current_tail = tail_.load(std::memory_order_relaxed);
        const size_t current_head = head_.load(std::memory_order_acquire);

        if ((current_tail - current_head) == Capacity) {
            return false; // Queue Penuh
        }

        buffer_[current_tail & (Capacity - 1)] = item;
        tail_.store(current_tail + 1, std::memory_order_release);
        return true;
    }

    // Konsumen (Hanya dipanggil oleh Consumer Strategy Thread)
    bool pop(T& item) {
        const size_t current_head = head_.load(std::memory_order_relaxed);
        const size_t current_tail = tail_.load(std::memory_order_acquire);

        if (current_head == current_tail) {
            return false; // Queue Kosong
        }

        item = buffer_[current_head & (Capacity - 1)];
        head_.store(current_head + 1, std::memory_order_release);
        return true;
    }

private:
    T buffer_[Capacity];

    // Penyelarasan Garis Cache 64-Byte untuk Menghilangkan Bencana 'False Sharing'!
    alignas(64) std::atomic<size_t> head_;
    alignas(64) std::atomic<size_t> tail_;
};

// Simulasi Tick Data Sederhana
struct MarketTick {
    uint64_t timestamp_ns;
    uint32_t symbol_id;
    int64_t price_cents;
    uint32_t size;
};
```""",
        "pitfalls": r"""*Bencana Flash Crash Akibat Ketiadaan Safety Checks (Kasus Knight Capital 2012)*: Dalam mengejar kecepatan eksekusi ekstrem, menghilangkan pemeriksaan batas risiko (*risk limit checks*) atau membiarkan kode lama aktif di sistem produksi dapat memicu bencana fatal. Knight Capital kehilangan $440 juta hanya dalam 45 menit akibat algoritma rusak yang terus-menerus membeli di harga penawaran tinggi dan menjual di harga murah jutaan kali secara otomatis. Selalu pasang *Pre-Trade Risk Checks* berbasis perangkat keras atau FPGA circuit breakers independen ([SEC Report on Knight Capital Failure](https://www.sec.gov/litigation/admin/2013/34-70694.pdf)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip C++ atau Python yang mendemonstrasikan fenomena *False Sharing*: buat dua thread yang secara intensif meningkatkan dua variabel integer dalam struct yang sama vs struct yang dipisahkan oleh padding 64 bytes (`alignas(64)`), ukur selisih waktu eksekusi clock CPU.
*Rubrik*: Versi terisolasi padding membuktikan peningkatan kecepatan eksekusi $> 2\times$.

### Level 2 (Menengah)
Bangun implementasi antrean melingkar bebas-kunci (*Lock-Free SPSC Ring Buffer*) lengkap di C++11/17: gunakan `std::atomic` dengan `memory_order_acquire/release`, lakukan pengujian benchmark pengiriman 10.000.000 pesan tick antar dua thread yang disematkan ke core prosesor terpisah via *CPU Pinning / Thread Affinity* (`pthread_setaffinity_np`).
*Rubrik*: Throughput mencapai $> 20.000.000$ pesan per detik tanpa ada data yang korup.

### Level 3 (Mahir)
Rancang arsitektur modul pengurai paket protokol pasar bursa NASDAQ ITCH 5.0 (pesan `Add Order 'A'`) di C++ atau Verilog: implementasikan parser berbasis zero-copy biner murni yang langsung memetakan pointer buffer jaringan `const char*` ke representasi struct bertipe tanpa memicu alokasi memori heap, dan ukur waktu latensi penguraian per paket ($< 25\text{ ns}$).
*Rubrik*: Parser tereksekusi bebas alokasi dinamis (`malloc == 0`) dan memvalidasi endianness jaringan.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Data Plane Development Kit (DPDK) Architecture Guide | Linux Foundation & Intel | [DPDK Official Documentation](https://doc.dpdk.org/) | Arsitektur Kernel-Bypass, HugePages, Poll-Mode Drivers |
| Concurrent Reading and Writing (Lock-Free Foundations) | Leslie Lamport (Turing Award Laureate) | [ACM Communications 1977](https://dl.acm.org/doi/10.1145/359642.359659) | Fondasi Asli Struktur Data Bebas Kunci SPSC |
| Flash Boys: A Wall Street Revolt | Michael Lewis | [W. W. Norton & Company](https://wwnorton.com/books/Flash-Boys/) | Investigasi Jurnalistik Mendalam Realitas Industri HFT & Kolokasi |
| Ultra-Low Latency Trading on FPGAs | Ehab Dehmamy et al. | [IEEE High Performance Extreme Computing](https://ieeexplore.ieee.org/document/8445123) | Desain Sirkuit Keras Tick-to-Trade Sub-Mikrodetik |"""
    },
    216: {
        "intuition": r"""Bagaimana sekelompok orang asing di seluruh dunia yang tidak saling mengenal dan tidak saling mempercayai bisa bersama-sama menyepakati satu buku besar keuangan tunggal tanpa ada bank, presiden, polisi, atau server pusat yang mengaturnya?

Satoshi Nakamoto memecahkan teka-teki legendaris ilmu komputer ini (**Masalah Para Jenderal Bizantium / Byzantine Generals Problem**) melalui penemuan **Blockchain & Konsensus Proof-of-Work (PoW)** ([Nakamoto - Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf)).

Bayangkan sebuah buku kas raksasa di mana setiap halaman buku (*blok*) berisi daftar ratusan transaksi keuangan. Untuk mengunci halaman tersebut agar tidak ada yang bisa memalsukannya:
1. Halaman tersebut dirangkum menggunakan rumus matematika sidik jari digital (**Pohon Merkle / Merkle Tree**) ([Merkle - A Certified Digital Signature](https://link.springer.com/chapter/10.1007/0-387-34799-2_32)).
2. Halaman baru harus mencantumkan sidik jari dari halaman sebelumnya, membentuk **Rantai Blok (Blockchain)**.
3. Para penambang (*miners*) harus menghabiskan miliaran daya listrik untuk memecahkan teka-teki kriptografi yang sangat sulit (*Proof-of-Work*) agar halaman mereka disetujui.

Vitalik Buterin kemudian memperluas ide ini menjadi **Ethereum Virtual Machine (EVM)**: tidak hanya mencatat angka transfer uang, blockchain bisa menjalankan kode program komputer abadi yang tidak bisa dimatikan oleh siapa pun (**Smart Contracts & DeFi**) ([Buterin - Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)).""",
        "theory": r"""Formulasi Kriptografi Blockchain & Keuangan Terdesentralisasi:

1. **Struktur Rantai Hash Monotonik & Pohon Merkle**:
Blok ke-$k$ didefinisikan sebagai tuple $\langle H_{k-1}, \text{MerkleRoot}, \text{Timestamp}, \text{Nonce}, \text{Transactions} \rangle$.
Pohon Merkle mengagregasikan $N$ transaksi secara hierarkis berpasangan via fungsi hash satu arah SHA-256:
$$H_{\text{parent}} = \text{Hash}(H_{\text{left}} \parallel H_{\text{right}})$$
*Bukti Keberadaan Merkle (Merkle Audit Proof)*: Memungkinkan verifikasi ringan (*Simplified Payment Verification / SPV*) apakah suatu transaksi berada di dalam blok dengan ukuran bukti logaritmik $\mathcal{O}(\log N)$ tanpa mengunduh seluruh transaksi blok.

2. **Konsensus Proof-of-Work (Nakamoto Consensus) vs Proof-of-Stake**:
* **PoW**: Mencari nilai acak *Nonce* sehingga nilai hash blok memenuhi ambang batas kesulitan (*Difficulty Target* $T$):
$$\text{SHA256}(\text{SHA256}(\text{BlockHeader})) < T$$
Probabilitas rantai terpanjang dikuasai oleh penyerang dengan kekuatan hashing fraksi $q < 0.5$ meluruh secara eksponensial seiring bertambahnya konfirmasi blok $z$:
$$P(\text{Double Spend}) = \sum_{k=0}^\infty \frac{\lambda^k e^{-\lambda}}{k!} \left( \frac{q}{p} \right)^{\max(z - k, 0)}, \quad \lambda = z \frac{q}{p}$$
* **PoS (Gasper / Casper FFG)**: Validator mempertaruhkan modal aset (32 ETH) dan mengamankan rantai melalui penalti pemotongan dana (*slashing*) jika terbukti menandatangani dua blok bercabang secara ganda ([Buterin & Griffith - Casper the Friendly Finality Gadget](https://arxiv.org/abs/1710.09437)).

3. **Mekanisme Automated Market Maker (AMM) Constant Product Uniswap v2**:
Kolam likuiditas terdesentralisasi memegang cadangan token $X$ dan token $Y$ dengan invarian fungsi konstan ([Adams et al. - Uniswap v2 Core](https://uniswap.org/whitepaper.pdf)):
$$x \cdot y = k$$
Jika pengguna menukar sejumlah $\Delta x$ token $X$ ke kolam dengan biaya transaksi $\gamma = 0.997$ (fee 0.3%), jumlah token $Y$ yang diterima ($\Delta y$):
$$(x + \gamma \Delta x)(y - \Delta y) = k \implies \Delta y = \frac{y \cdot \gamma \Delta x}{x + \gamma \Delta x}$$
Harga marginal spot: $P = \frac{y}{x}$, dengan *Slippage* yang tumbuh proporsional terhadap ukuran pertukaran $\frac{\Delta x}{x}$.""",
        "internals": r"""Arsitektur State Transition Function pada Ethereum Virtual Machine (EVM):

```mermaid
flowchart TD
    State_t["World State S_t (Merkle Patricia Trie: Akun, Saldo, Storage)"] --> Tx["Transaksi: Kirim Bytecode / Panggilan Smart Contract"]
    Tx --> EVM["Mesin Virtual EVM (Stack 256-bit, Gas Metering, Opcode Execution)"]
    
    subgraph Execution["EVM Sandbox Execution"]
        GasCheck["Periksa Kuota Gas Limit (Mencegah Halting Problem)"]
        Opcodes["Eksekusi Opcode: SLOAD, SSTORE, ADD, SHA3"]
        GasCheck --> Opcodes
    end
    
    EVM --> Execution
    Execution --> State_t1["World State Baru S_t+1 (Append-Only Hash Root)"]
```

EVM beroperasi sebagai mesin status Turing-Complete kuasi-deterministik: setiap instruksi komputasi mengenakan biaya bahan bakar (*Gas*) yang harus dibayar pengirim, menyelesaikan masalah *Halting Problem* secara elegan (program dengan infinite loop akan mati kehabisan gas secara otomatis) ([Wood - Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)).""",
        "code_block": r"""```python
import hashlib

# 1. Implementasi Pohon Merkle Kriptografis dari Nol
def sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, transactions: list[str]):
        self.transactions = transactions
        self.tree_levels = []
        self._build_tree()
        
    def _build_tree(self):
        current_level = [sha256(tx) for tx in self.transactions]
        self.tree_levels.append(current_level)
        
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if (i + 1 < len(current_level)) else left
                combined_hash = sha256(left + right)
                next_level.append(combined_hash)
            current_level = next_level
            self.tree_levels.append(current_level)
            
    def get_root(self) -> str:
        return self.tree_levels[-1][0] if self.tree_levels else ""

# 2. Rumus Pertukaran Token AMM Constant Product Uniswap v2
def uniswap_v2_swap(x_reserve, y_reserve, dx_input, fee=0.003):
    # dx_net = dx * (1 - fee)
    dx_net = dx_input * (1.0 - fee)
    # (x + dx_net) * (y - dy) = x * y
    dy_output = (y_reserve * dx_net) / (x_reserve + dx_net)
    new_x = x_reserve + dx_input
    new_y = y_reserve - dy_output
    price_impact = (dx_input / x_reserve) * 100
    return dy_output, new_x, new_y, price_impact

# Uji Coba Merkle Tree
txs = ["Alice->Bob: 5 BTC", "Charlie->Dave: 2 BTC", "Eve->Frank: 10 BTC", "Grace->Heidi: 1 BTC"]
mt = MerkleTree(txs)
print(f"Merkle Root (Sidik Jari 4 Transaksi): {mt.get_root()}")

# Uji Coba AMM Uniswap v2 Pool (1.000 ETH dan 2.000.000 USDC)
eth_res, usdc_res = 1_000.0, 2_000_000.0
usdc_out, new_eth, new_usdc, slippage = uniswap_v2_swap(eth_res, usdc_res, dx_input=10.0)

print(f"\nSwap 10 ETH ke Uniswap Pool:")
print(f"USDC Diterima Pengguna : ${usdc_out:,.2f} USDC (Rata-rata: ${usdc_out/10:,.2f}/ETH)")
print(f"Harga Spot Awal        : ${usdc_res / eth_res:,.2f}/ETH")
print(f"Slippage / Price Impact: {slippage:.2f}%")
```""",
        "pitfalls": r"""*Kerentanan Serangan Reentrancy pada Smart Contract (Bencana The DAO)*: Dalam kode Solidity, jika kontrak mentransfer koin ether ke alamat pengguna eksternal sebelum memperbarui catatan saldo internalnya (`msg.sender.call{value: amount}("")`), kontrak penerima yang jahat dapat menulis fungsi fallback yang memanggil kembali fungsi penarikan tersebut (*re-entrant call*) secara rekursif sebelum saldo berkurang, menguras seluruh dana kas kontrak. Selalu terapkan pola desain **Checks-Effects-Interactions** atau gunakan ReentrancyGuard mutex ([Atzei et al. - A Survey of Attacks on Ethereum Smart Contracts](https://link.springer.com/chapter/10.1007/978-3-662-54455-6_8)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis simulasi algoritma penambangan konsensus Proof-of-Work (PoW) sederhana di Python: terima data string blok, lakukan hashing berulang dengan incrementing nonce hingga menemukan hash SHA-256 yang diawali oleh 4 karakter nol ("0000"), dan catat total iterasi serta waktu komputasi yang dibutuhkan.
*Rubrik*: Output mencetak nonce pemenang dan hash valid yang memenuhi target kesulitan.

### Level 2 (Menengah)
Implementasikan struktur Pohon Merkle lengkap beserta fungsi pembuatan bukti audit (*Merkle Proof Generator*) dan verifikasi bukti (*Merkle Proof Verifier*): buktikan bahwa simpul daun dapat divalidasi keabsahannya terhadap Merkle Root hanya menggunakan deretan hash tetangga tanpa mengetahui isi daun lainnya.
*Rubrik*: Fungsi verifikator mengembalikan `True` untuk bukti yang sah dan `False` jika data dipalsukan.

### Level 3 (Mahir)
Bangun smart contract Automated Market Maker (AMM) Uniswap v2 mini menggunakan bahasa Solidity atau simulator komputasional Python lengkap: implementasikan fungsi penambahan likuiditas (`mint` LP Token berbasis $\sqrt{x \cdot y}$), fungsi penghapusan likuiditas (`burn`), dan fungsi pertukaran (`swap`) dengan proteksi reentrancy lock.
*Rubrik*: Invarian produk konstan terverifikasi meningkat secara monotonik akibat akumulasi fee transaksi.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Bitcoin: A Peer-to-Peer Electronic Cash System | Satoshi Nakamoto | [Bitcoin Whitepaper PDF](https://bitcoin.org/bitcoin.pdf) | Makalah Penemuan Blockchain Asli, Proof-of-Work, Konsensus |
| Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform | Vitalik Buterin | [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/) | Konsep Mesin Virtual EVM, Smart Contracts, Gas Metering |
| Uniswap v2 Core Whitepaper | Hayden Adams, Noah Zinsmeister, Dan Robinson | [Uniswap Official Whitepaper](https://uniswap.org/whitepaper.pdf) | Matematika Constant Product Market Maker AMM, Invarian xy=k |
| Ethereum Yellow Paper: The Formal Specification of Ethereum | Gavin Wood (Polkadot Founder) | [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf) | Spesifikasi Matematis Formal Opcode EVM & Merkle Patricia Trie |"""
    }
}
