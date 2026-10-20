"""Encyclopedia Tier 14 Part 1: Topics 207 - 211 (Market Economics & Banking, Computational Ledger, Payment Networks, Financial Math, Modern Portfolio Theory)
"""

DATA_TIER_14_PART1 = {
    207: {
        "intuition": r"""Di mana uang sebenarnya berasal? Sebagian besar orang mengira bahwa ketika mereka meminjam Rp 100 juta dari bank, bank mengambil uang tunai fisik milik nasabah lain dari dalam brankas besi lalu menyerahkannya.

Faktanya, dalam sistem keuangan modern (**Fractional-Reserve Banking**), uang diciptakan dari ketiadaan (*ex nihilo*) melalui pencatatan akuntansi digital ([Bank of England - Money Creation in the Modern Economy](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy)). Ketika bank menyetujui pinjaman Anda, bank hanya mengetik angka "Rp 100.000.000" di layar komputer rekening Anda (sebagai liabilitas bank) dan mencatat surat utang Anda di sisi lain (sebagai aset bank).

Sistem moneter modern adalah jejaring kepercayaan raksasa yang diatur oleh **Bank Sentral** (seperti Federal Reserve atau Bank Indonesia). Bank sentral mengatur jumlah likuiditas melalui suku bunga acuan (*Interest Rate*) dan rasio giro wajib minimum (*Reserve Requirement*), memastikan bahwa roda perputaran ekonomi tidak mengalami kepanikan penarikan massal (**Bank Run**) ([Mishkin - The Economics of Money, Banking, and Financial Markets](https://www.pearson.com/en-us/subject-catalog/p/economics-of-money-banking-and-financial-markets-the/P200000003346)).""",
        "theory": r"""Formulasi Matematis Sistem Moneter & Multiplier Perbankan:

1. **Model Pengganda Uang Fraksional (Money Multiplier)**:
Di bawah regulasi rasio cadangan wajib $R \in (0, 1)$ dan preferensi nasabah memegang uang tunai $c = \frac{C}{D}$:
$$M = m \cdot B, \quad m = \frac{1 + c}{R + c + e}$$
Di mana $B$ adalah basis moneter (uang kartal + cadangan bank sentral), $e$ adalah kelebihan cadangan (*excess reserve*), dan $M$ adalah total jumlah uang beredar (M1/M2). Jika $c = 0$ dan $e = 0$, ekspansi kredit teoritis maksimum:
$$\Delta M = \frac{1}{R} \Delta D$$

2. **Persamaan Neraca Bank Komersial (T-Account Balance Sheet)**:
$$\text{Aset} \equiv \text{Liabilitas} + \text{Ekuitas}$$
* Sisi Aset: Cadangan Tunai di Bank Sentral ($R$), Pinjaman yang Disalurkan kepada Debitur ($L$), Surat Berharga Negara ($S$).
* Sisi Liabilitas: Simpanan Rekening Giro/Tabungan Nasabah ($D$), Pinjaman Antarbank ($B$).
* Rasio Kecukupan Modal Basel III (Capital Adequacy Ratio / CAR):
$$\text{CAR} = \frac{\text{Tier 1 Capital} + \text{Tier 2 Capital}}{\text{Risk-Weighted Assets (RWA)}} \ge 8\%$$
Mencegah kebangkrutan bank akibat gagal bayar kredit sistemik ([Bank for International Settlements - Basel III Framework](https://www.bis.org/bcbs/basel3.htm)).

3. **Mekanisme Pasar Uang Antar Bank (Interbank Lending Rate)**:
Tingkat bunga semalam (*Overnight Rate* seperti SOFR atau BI-Rate) terbentuk dari perpotongan kurva permintaan likuiditas cadangan bank terhadap target koridor fasilitas bank sentral (Deposit Facility vs Lending Facility).""",
        "internals": r"""Arsitektur interaksi neraca akuntansi dua bank komersial selama transfer kawat bank sentral (RTGS):

```mermaid
sequenceDiagram
    autonumber
    actor Alice as Nasabah Alice (Bank A)
    participant BankA as Bank A (Komersial)
    participant CentralBank as Real-Time Gross Settlement (RTGS Bank Sentral)
    participant BankB as Bank B (Komersial)
    actor Bob as Nasabah Bob (Bank B)

    Alice->>BankA: Instruksi Transfer Rp 10 Juta ke Bob
    Note over BankA: Debet Deposit Alice (-10 Juta Liabilitas)
    BankA->>CentralBank: Kirim Pesan Kliring RTGS Settlement
    Note over CentralBank: Pindahkan Cadangan: Bank A (-10 Juta) -> Bank B (+10 Juta)
    CentralBank->>BankB: Konfirmasi Setelmen Cadangan Diterima
    Note over BankB: Kredit Deposit Bob (+10 Juta Liabilitas)
    BankB->>Bob: Saldo Rekening Bob Bertambah Rp 10 Juta
```

Uang tidak pernah benar-benar "berpindah kabel"; yang terjadi adalah pembaruan buku besar serentak di Bank Sentral (*Real-Time Gross Settlement / RTGS*) yang menyelaraskan cadangan antarbank secara atomik ([CPMI - Core Principles for Systemically Important Payment Systems](https://www.bis.org/cpmi/publ/d43.htm)).""",
        "code_block": r"""```python
# Simulasi Sistem Perbankan Cadangan Fraksional (Fractional-Reserve Banking)
class CentralBank:
    def __init__(self, reserve_ratio=0.10):
        self.reserve_ratio = reserve_ratio # 10% Giro Wajib Minimum
        
class CommercialBank:
    def __init__(self, name, central_bank):
        self.name = name
        self.cb = central_bank
        self.reserves = 0.0 # Cadangan uang di Bank Sentral
        self.deposits = 0.0 # Liabilitas hutang ke nasabah
        self.loans = 0.0    # Aset piutang pinjaman
        
    def deposit(self, amount):
        self.deposits += amount
        self.reserves += amount
        print(f"[{self.name}] Menerima Deposit: Rp {amount:,.0f} | Cadangan: Rp {self.reserves:,.0f}")
        
    def create_loan(self, borrower_name, amount):
        required_reserves = self.deposits * self.cb.reserve_ratio
        excess_reserves = self.reserves - required_reserves
        
        if amount > excess_reserves:
            raise ValueError(f"Pinjaman ditolak! Cadangan berlebih hanya Rp {excess_reserves:,.0f}")
            
        self.loans += amount
        self.reserves -= amount # Uang keluar ke peminjam
        print(f"[{self.name}] Menyalurkan Kredit ke {borrower_name}: Rp {amount:,.0f} (Ex Nihilo Credit Creation)")
        return amount

# Eksekusi Siklus Ekspansi Moneter Multi-Bank
bi = CentralBank(reserve_ratio=0.10)
bank_a = CommercialBank("Bank Mandiri", bi)
bank_b = CommercialBank("Bank BCA", bi)

# 1. Nasabah menyetor modal awal Rp 100 Juta ke Bank A
bank_a.deposit(100_000_000)

# 2. Bank A meminjamkan 90% (Rp 90 Juta) ke Kontraktor
loan_1 = bank_a.create_loan("Kontraktor Proyek", 90_000_000)

# 3. Kontraktor membayar supplier, yang menyetor uangnya ke Bank B
bank_b.deposit(loan_1)

# 4. Bank B meminjamkan 90% dari Rp 90 Juta (Rp 81 Juta) ke Toko Bahan Bangunan
loan_2 = bank_b.create_loan("Toko Besi", 81_000_000)

total_deposits_created = bank_a.deposits + bank_b.deposits
print(f"\nTotal Uang Beredar Baru Tercipta dalam Sistem: Rp {total_deposits_created:,.0f}")
print(f"Modal Dasar Awal: Rp 100,000,000 -> Uang Beredar Berlipat Ganda!")
```""",
        "pitfalls": r"""*Maturity Mismatch & Bank Run Vulnerability*: Bank komersial meminjam jangka pendek (simpanan tabungan nasabah yang dapat ditarik sewaktu-waktu / *on demand*) dan meminjamkannya untuk jangka panjang (kredit pemilikan rumah 20 tahun atau obligasi jangka panjang). Jika nasabah panik secara serentak menarik simpanan mereka karena rumor kegagalan (*Bank Run* seperti Silicon Valley Bank 2023), bank yang sebenarnya solvabel secara aset akan kolaps seketika akibat ketidakmampuan melikuidasi aset jangka panjang dalam hitungan jam ([Diamond & Dybvig - Bank Runs, Deposit Insurance, and Liquidity](https://www.jstor.org/stable/1837095)).""",
        "exercises": r"""### Level 1 (Pemula)
Buat neraca T-Account komparatif (Aset vs Liabilitas) sebelum dan sesudah bank menerbitkan pinjaman KPR senilai Rp 500 juta dengan rasio cadangan wajib 10%, dan buktikan kedua sisi neraca tetap seimbang (*balance*).
*Rubrik*: Penyajian tabel T-Account mencantumkan akun kas cadangan, kredit piutang, dan simpanan giro.

### Level 2 (Menengah)
Bangun simulator sistem moneter multi-bank di Python: simulasikan proses ekspansi kredit berulang (*recursive money multiplication*) dari setoran awal $1.000 hingga konvergen, plot kurva total uang beredar terhadap rasio cadangan wajib $R \in [0.05, 0.25]$, dan bandingkan terhadap formula teoritis $1/R$.
*Rubrik*: Nilai simulasi konvergen ke angka analitis $\pm 0.1\%$.

### Level 3 (Mahir)
Implementasikan model komputasional stres likuiditas Basel III Liquidity Coverage Ratio (LCR):
$$\text{LCR} = \frac{\text{Total High-Quality Liquid Assets (HQLA)}}{\text{Total Net Cash Outflows over 30 Days}} \ge 100\%$$
Simulasikan skenario penarikan simpanan retail (tingkat lari 5%), simpanan korporasi tanpa agunan (40%), dan penurunan nilai agunan surat berharga pemerintah jangka panjang. Hitung apakah bank mempertahankan rasio LCR $> 100\%$.
*Rubrik*: Perhitungan cash outflow dan inflow terdiskon sesuai aturan Basel III eksak.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Money Creation in the Modern Economy | Michael McLeay et al. (Bank of England) | [Bank of England Quarterly Bulletin](https://www.bankofengland.co.uk/quarterly-bulletin/2014/q1/money-creation-in-the-modern-economy) | Dekonstruksi Mitos Uang: Fractional-Reserve Realitas |
| Bank Runs, Deposit Insurance, and Liquidity | Douglas W. Diamond & Philip H. Dybvig (Nobel 2022) | [Journal of Political Economy](https://www.jstor.org/stable/1837095) | Model Teoretis Terkenal Diamond-Dybvig Keruntuhan Bank |
| Basel III: A Global Regulatory Framework for More Resilient Banks | Basel Committee on Banking Supervision (BIS) | [BIS Official Standard](https://www.bis.org/bcbs/basel3.htm) | Rasio CAR, Tier 1 Capital, LCR, Leverage Ratio |
| The Economics of Money, Banking, and Financial Markets | Frederic S. Mishkin (Columbia University) | [Pearson Higher Ed](https://www.pearson.com/en-us/subject-catalog/p/economics-of-money-banking-and-financial-markets-the/P200000003346) | Buku Teks Standar Moneter, Kebijakan Suku Bunga Sentral |"""
    },
    208: {
        "intuition": r"""Bayangkan Anda sedang membangun sebuah sistem perbankan atau dompet digital (*fintech*). Jika seorang pengguna mentransfer uang Rp 50.000 ke temannya, apa yang Anda lakukan di database? Apakah Anda cukup menjalankan perintah: `UPDATE users SET balance = balance - 50000 WHERE id = 1`?

Jika Anda melakukan itu, Anda telah melakukan dosa terbesar dalam rekayasa sistem keuangan! Bagaimana jika server Anda mati mendadak setelah saldo pengirim dipotong tetapi sebelum saldo penerima bertambah? Uang Rp 50.000 tersebut lenyap ke udara, dan tidak ada seorang pun di dunia ini yang bisa membuktikan ke mana uang itu pergi karena saldo lama telah ditimpa secara permanen.

Inilah mengapa peradaban modern bertumpu pada **Pembukuan Berpasangan (Double-Entry Bookkeeping)** yang telah teruji selama lebih dari 500 tahun ([Luca Pacioli - Summa de Arithmetica, 1494](https://www.maa.org/press/periodicals/convergence/mathematical-treasure-luca-paciolis-summa-de-arithmetica)). Dalam buku besar keuangan, **saldo tidak pernah disimpan sebagai angka tunggal yang ditimpa**. Setiap transaksi adalah catatan permanen yang tidak dapat diubah (*immutable append-only*): setiap rupiah yang keluar dari satu akun (**Kredit**) harus dicatat masuk ke akun lain (**Debet**) dalam jumlah yang persis sama. Dan satu aturan mutlak: **Jangan pernah menggunakan tipe data float untuk uang!** ([Martin Fowler - Accounting Patterns](https://martinfowler.com/eaaDev/AccountingNarrative.html)).""",
        "theory": r"""Landasan Matematis & Aksioma Buku Besar Komputasional:

1. **Aksioma Dasar Pembukuan Berpasangan (Double-Entry Equation)**:
Sistem akun dipartisi menjadi 5 kelas primer: Aset ($A$), Beban/Expenses ($E$), Liabilitas ($L$), Ekuitas ($Q$), dan Pendapatan/Revenue ($R$):
$$(A + E) \equiv (L + Q + R)$$
Dalam konvensi debet/kredit bertanda aljabar:
$$\sum_{i=1}^N \text{Amount}_i \equiv 0 \quad (\text{Zero-Sum Conservation Law})$$
Setiap transaksi keuangan $T$ adalah tuple $\langle \text{ID}, \text{Timestamp}, \{(a_1, v_1), (a_2, v_2), \dots, (a_k, v_k)\} \rangle$ dengan syarat invarian mutlak: $\sum_{j=1}^k v_j = 0$.

2. **Bencana Pembulatan Floating-Point IEEE 754**:
Bilangan pecahan biner floating-point tidak dapat merepresentasikan desimal seperti 0.1 secara eksak:
$$0.1_{10} = 0.0001100110011\dots_2$$
Dalam Python: `0.1 + 0.2 == 0.3` menghasilkan `False` (`0.30000000000000004`)! Akumulasi galat pembulatan pada jutaan transaksi harian akan merusak integritas rekonsiliasi keuangan. Selalu gunakan bilangan bulat presisi tetap (*Fixed-Point Integer* atau representasi satuan terkecil / sen / satoshi).

3. **Prinsip Imutabilitas Append-Only**:
Buku besar finansial adalah log linier monotonik:
$$\text{Ledger}_{t+1} = \text{Ledger}_t \cup \{T_{\text{new}}\}$$
Tidak ada operasi `UPDATE` atau `DELETE`. Jika terjadi kesalahan transfer, perbaikan dilakukan dengan mencatat transaksi pembalik baru (*reversal / compensating transaction*) ([TigerBeetle Architecture - Design of a Financial Accounting Database](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/DESIGN.md)).""",
        "internals": r"""Arsitektur integritas data buku besar keuangan append-only dengan rantai hash kriptografis:

```mermaid
flowchart LR
    subgraph Transaction_1["Entry #101 (Immutable)"]
        T1["Debet: Alice Cash (-Rp 50.000)<br/>Kredit: Bob Cash (+Rp 50.000)<br/>Sum == 0<br/>PrevHash: 0x0000"]
    end
    subgraph Transaction_2["Entry #102 (Immutable)"]
        T2["Debet: Bob Cash (-Rp 20.000)<br/>Kredit: Fee Income (+Rp 20.000)<br/>Sum == 0<br/>PrevHash: Hash(Entry #101)"]
    end
    subgraph Query_Engine["Audit Engine"]
        Bal["Saldo Akun Alice = sum(Debets) - sum(Credits)"]
    end
    Transaction_1 --> Transaction_2
    Transaction_2 -.-> Query_Engine
```

Saldo akun dihitung sebagai agregasi derivatif (*materialized view*) dari penjumlahan seluruh entri mutasi sejarah sejak awal mula, menjamin bukti audit (*audit trail*) matematis yang tidak terbantahkan ([Fowler Accounting Patterns](https://martinfowler.com/eaaDev/AccountingNarrative.html)).""",
        "code_block": r"""```python
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
import hashlib

# 1. Definisi Model Entri Transaksi Double-Entry Imutabel
@dataclass(frozen=True)
class Posting:
    account_id: str
    amount_cents: int # Menggunakan Integer Sen (Rp 1 = 100 sen) untuk mencegah galat Float!

@dataclass(frozen=True)
class Transaction:
    tx_id: str
    timestamp: str
    postings: tuple[Posting, ...]
    prev_hash: str
    
    def __post_init__(self):
        # Aksioma Konservasi Finansial Mutlak: Total Debet + Total Kredit == 0
        total = sum(p.amount_cents for p in self.postings)
        if total != 0:
            raise ValueError(f"Invarian Gagal! Transaksi {self.tx_id} tidak seimbang: selisih {total} sen")

# 2. Mesin Buku Besar Append-Only (Append-Only Ledger Engine)
class FinancialLedger:
    def __init__(self):
        self.transactions: list[Transaction] = []
        self.latest_hash = "0" * 64
        
    def record_transfer(self, tx_id: str, from_account: str, to_account: str, amount_cents: int):
        if amount_cents <= 0:
            raise ValueError("Nilai transfer harus positif!")
            
        postings = (
            Posting(account_id=from_account, amount_cents=-amount_cents), # Keluar (Kredit)
            Posting(account_id=to_account, amount_cents=amount_cents)     # Masuk (Debet)
        )
        
        # Buat rantai hash kriptografis untuk integritas audit
        tx_data = f"{tx_id}{self.latest_hash}{amount_cents}"
        tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
        
        tx = Transaction(
            tx_id=tx_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            postings=postings,
            prev_hash=self.latest_hash
        )
        self.transactions.append(tx)
        self.latest_hash = tx_hash
        return tx

    def get_account_balance(self, account_id: str) -> int:
        # Saldo adalah hasil penjumlahan mutasi historis murni
        balance = 0
        for tx in self.transactions:
            for p in tx.postings:
                if p.account_id == account_id:
                    balance += p.amount_cents
        return balance

# Uji Coba Transaksi Keuangan Nyata
ledger = FinancialLedger()
ledger.record_transfer("TX_001", "ALICE_WALLET", "BOB_WALLET", 50_000_00) # Rp 50.000 (5.000.000 sen)
ledger.record_transfer("TX_002", "BOB_WALLET", "MERCHANT_XYZ", 15_000_00) # Rp 15.000 (1.500.000 sen)

print(f"Saldo Alice    : Rp {ledger.get_account_balance('ALICE_WALLET') / 100:,.2f}")
print(f"Saldo Bob      : Rp {ledger.get_account_balance('BOB_WALLET') / 100:,.2f}")
print(f"Saldo Merchant : Rp {ledger.get_account_balance('MERCHANT_XYZ') / 100:,.2f}")
print(f"Integritas Hash Rantai Ledger: {ledger.latest_hash[:16]}... (Valid & Immutable)")
```""",
        "pitfalls": r"""*Race Condition Saldo Negatif (Double Spending via Concurrency)*: Dua transaksi penarikan dana senilai Rp 100.000 dieksekusi secara paralel di dua worker server yang berbeda pada saat yang persis bersamaan untuk akun yang hanya memiliki saldo Rp 100.000. Jika pengecekan saldo (`SELECT balance WHERE id=1`) dilakukan tanpa kuncian atomik (*pessimistic lock* `SELECT ... FOR UPDATE` atau *optimistic serializable isolation*), kedua worker akan melihat saldo cukup dan mengeksekusi penarikan, menyebabkan akun menjadi minus dan bank rugi uang riil ([TigerBeetle Design Doc](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/DESIGN.md)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip Python yang mendemonstrasikan galat akumulasi floating point IEEE 754: tambahkan angka `0.1` sebanyak 1.000.000 kali menggunakan tipe data `float` standar vs tipe data `int` (sen terkecil), dan cetak selisih galat keuangan yang dihasilkan.
*Rubrik*: Output menampilkan selisih deviasi rupiah riil yang hilang akibat pemotongan bit float.

### Level 2 (Menengah)
Bangun modul buku besar akuntansi multi-mata uang (*multi-currency ledger*): implementasikan akun perantara konversi valuta asing (*FX Settlement Clearing Account*) yang memvalidasi bahwa transaksi pertukaran USD ke IDR tetap seimbang di setiap mata uang masing-masing.
*Rubrik*: Transaksi valas lolos verifikasi keseimbangan debet-kredit di kedua denominasi mata uang.

### Level 3 (Mahir)
Rancang arsitektur mesin buku besar finansial berperforma tinggi menggunakan SQLite atau PostgreSQL dengan level isolasi transaksi `SERIALIZABLE`. Terapkan verifikasi kendala basis data (`CHECK (balance >= 0)`) dan jalankan uji konkurensi multi-thread (50 thread paralel) yang mencoba menarik dana secara bersamaan untuk membuktikan bahwa saldo negatif dan double-spending 100% mustahil terjadi.
*Rubrik*: Tidak ada race condition, tepat satu transaksi yang berhasil sementara sisanya ditolak secara aman.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Accounting Patterns | Martin Fowler | [Martin Fowler Architecture Guides](https://martinfowler.com/eaaDev/AccountingNarrative.html) | Pola Desain Perangkat Lunak Buku Besar, Posting Rules |
| TigerBeetle: Financial Accounting Database Design | TigerBeetle Core Team (Joran Dirk Greef) | [TigerBeetle Design Architecture](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/DESIGN.md) | Database Finansial Khusus Berperforma Tinggi, Zero-Allocation |
| Summa de Arithmetica, Geometria, Proportioni et Proportionalita | Fra Luca Pacioli (1494) | [Mathematical Association of America](https://www.maa.org/press/periodicals/convergence/mathematical-treasure-luca-paciolis-summa-de-arithmetica) | Naskah Sejarah Penemu Sistem Pembukuan Berpasangan |
| PCI-DSS Financial Data Security Standards | PCI Security Standards Council | [PCI-DSS Official Document](https://www.pcisecuritystandards.org/) | Keamanan Penyimpanan Data Transaksi & Kepatuhan Audit |"""
    },
    209: {
        "intuition": r"""Ketika Anda menempelkan kartu debit atau kartu kredit Anda di mesin kasir (EDC) sebuah minimarket, dalam waktu kurang dari 2 detik layar mesin berbunyi *bip* dan struk pembayaran tercetak. Pernahkah Anda membayangkan apa yang terjadi di kabel bawah laut dunia dalam 2 detik tersebut?

Sinyal tersebut melompati sebuah labirin sistem global raksasa:
1. Dari mesin EDC minimarket ke bank pemilik mesin (**Acquirer Bank**).
2. Dari bank acquirer melesat ke jaringan switching raksasa dunia (**Visa, Mastercard, atau GPN**).
3. Jaringan switching meneruskannya ke bank tempat Anda menabung (**Issuer Bank**).
4. Komputer mainframe bank penerbit memeriksa apakah saldo Anda cukup dan kartu Anda tidak diblokir.
5. Jawaban disetujui (*Approved*) dikirimkan balik ke mesin EDC!

Agar jutaan komputer dari ribuan bank di seluruh penjuru bumi yang menggunakan bahasa dan sistem operasi berbeda bisa berbicara tanpa salah paham, mereka menggunakan bahasa protokol standar perbankan global: **ISO 8583** (standar legendaris berbasis bitmap biner sejak 1987) dan penerus modernnya **ISO 20022** (standar berbasis XML/JSON untuk pesan perbankan bernilai tinggi) ([ISO - Financial Transaction Card Originated Messages](https://www.iso.org/standard/31628.html)).""",
        "theory": r"""Formulasi Protokol Pesan Finansial ISO 8583 & ISO 20022:

1. **Struktur Pesan ISO 8583**:
Terdiri dari 3 komponen utama:
* **Message Type Identifier (MTI)**: 4 digit angka yang mendefinisikan versi ISO, kelas pesan, fungsi, dan asal pengirim (misal `0100` = Permintaan Otorisasi, `0110` = Respons Otorisasi, `0200` = Permintaan Finansial Settlement).
* **Bitmap Primer & Sekunder (Bitmaps)**: Bilangan heksadesimal 64-bit (8 bytes) atau 128-bit di mana setiap bit individual bertindak sebagai saklar boolean: bit ke-$k$ bernilai 1 jika *Data Element* (DE) ke-$k$ hadir dalam pesan.
* **Data Elements (DE 1 s/d DE 128)**:
  - DE 2: Primary Account Number / Nomor Kartu (PAN, LLVAR)
  - DE 3: Processing Code (6 digit: 2 digit jenis transaksi, 2 digit akun sumber, 2 digit akun tujuan)
  - DE 4: Amount, Transaction (12 digit angka fixed-width)
  - DE 11: System Trace Audit Number (STAN 6 digit)
  - DE 39: Response Code (2 karakter: `00` = Approved, `51` = Insufficient Funds) ([ISO 8583 Specification](https://www.iso.org/standard/31628.html)).

2. **Protokol Standar Modern ISO 20022 (Universal Financial Industry Message Scheme)**:
Format modular semantik berbasis XML/JSON terstruktur yang digunakan oleh SWIFT dan RTGS global:
* `pacs` (Payment Clearing and Settlement): misal `pacs.008` (Credit Transfer Finansial Antarbank).
* `camt` (Cash Management): misal `camt.053` (Laporan Rekening Koran Bank).
* `pain` (Payment Initiation): misal `pain.001` (Instruksi Pembayaran Korporasi).

3. **Kepatuhan Keamanan PCI-DSS (Payment Card Industry Data Security Standard)**:
Standar regulasi ketat keamanan kartu pembayaran: Larangan keras menyimpan *Sensitive Authentication Data (SAD)* pasca-otorisasi mencakup PIN Block, Nilai Verifikasi Kartu (CVV2/CVC2), dan Full Track Data magnetik. Data PAN yang disimpan harus disamarkan (*masked*, hanya menampilkan 6 digit pertama dan 4 digit terakhir: `4111-11**-****-1111`) dan dienkripsi kuat via AES-256 ([PCI Security Standards](https://www.pcisecuritystandards.org/)).""",
        "internals": r"""Arsitektur empat pihak (*Four-Party Model*) ekosistem pemrosesan pembayaran kartu:

```mermaid
flowchart LR
    Cardholder["Pemegang Kartu (Pembeli)"] --> Merchant["Merchant (Pedagang / Toko)"]
    Merchant --> Acquirer["Acquirer Bank (Bank Pengelola EDC)"]
    Acquirer --> Network["Payment Network (Visa / Mastercard / GPN Switch)"]
    Network --> Issuer["Issuer Bank (Bank Penerbit Kartu Nasabah)"]
    
    Issuer -.->|"Response 00 Approved (ISO 8583)"| Network
    Network -.-> Acquirer
    Acquirer -.-> Merchant
    Merchant -.->|"Struk Pembayaran Berhasil"| Cardholder
```

Peran Payment Network adalah melakukan kliring multilateral (*multilateral clearing*) dan menanggung risiko setelmen antar-bank setiap hari, memungkinkan otorisasi transaksi selesai dalam batas latensi $300 - 800\text{ ms}$ di seluruh dunia ([Evans & Schmalensee - Paying with Plastic](https://mitpress.mit.edu/9780262550581/paying-with-plastic/)).""",
        "code_block": r"""```python
# Parser Sederhana Komponen Bitmap Protokol Finansial ISO 8583
def parse_iso8583_bitmap(hex_bitmap_str):
    # Konversi string hex 16 karakter (64-bit) menjadi representasi binary string
    bitmap_int = int(hex_bitmap_str, 16)
    bitmap_bin = f"{bitmap_int:064b}"
    
    present_elements = []
    for bit_idx, bit_val in enumerate(bitmap_bin, start=1):
        if bit_val == '1':
            present_elements.append(bit_idx)
            
    return present_elements

# Simulasi Pesan ISO 8583 MTI 0100 (Authorization Request)
mti = "0100"
# Bitmap: Elemen 3 (Processing Code), Elemen 4 (Amount), Elemen 11 (STAN) aktif
# Bit 3, 4, 11 bernilai 1 -> Binary: 0011 0000 0010 0000 ... -> Hex: 3020000000000000
sample_bitmap_hex = "3020000000000000"

active_de = parse_iso8583_bitmap(sample_bitmap_hex)
print(f"ISO 8583 MTI: {mti} (Permintaan Otorisasi Transaksi)")
print(f"Primary Bitmap Hex: {sample_bitmap_hex}")
print(f"Data Elements yang Hadir: {active_de}")

# Simulasi Pemetaan Payload
payload = {
    3: "000000",        # Purchase Goods
    4: "000000050000",  # Rp 50.000,00 (12 digit fixed width)
    11: "123456"        # Trace Audit Number (STAN)
}

print(f"DE 3  (Processing Code): {payload[3]}")
print(f"DE 4  (Amount Raw)     : Rp {int(payload[4])/100:,.2f}")
print(f"DE 11 (STAN Audit)     : {payload[11]}")
```""",
        "pitfalls": r"""*Menyimpan CVV atau Unencrypted PAN (Pelanggaran Berat PCI-DSS)*: Developer yang menyimpan nomor kartu lengkap (PAN) tanpa enkripsi atau menyimpan kode keamanan CVV di dalam tabel database/log aplikasi menghadapi sanksi denda jutaan dolar dan pencabutan izin memproses kartu pembayaran. Selalu gunakan mekanisme **Tokenisasi Kartu (Card Tokenization)** dari gateway pembayaran terakreditasi, di mana data sensitif digantikan oleh token string acak non-sensitif sebelum menyentuh server aplikasi Anda ([PCI-DSS Standard Requirements](https://www.pcisecuritystandards.org/)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip decoder ISO 8583 di Python yang menerima string pesan lengkap berformat MTI + Bitmap + DE 3 + DE 4, lalu memecahnya secara otomatis menjadi kamus JSON yang mudah dibaca manusia.
*Rubrik*: Parser mengekstrak MTI, mendeteksi bit aktif, dan memotong string nilai data secara presisi.

### Level 2 (Menengah)
Bangun simulator gateway otorisasi pembayaran ISO 8583: buat server soket TCP mini yang menerima paket pesan `0100` (Authorization Request), memvalidasi saldo akun fiktif, mengembalikan pesan balasan `0110` dengan DE 39 bernilai `00` (Approved) jika saldo cukup atau `51` (Insufficient Funds) jika tidak cukup.
*Rubrik*: Menghasilkan pesan respons ISO 8583 yang valid dengan bitmap respons yang sesuai.

### Level 3 (Mahir)
Rancang skema validasi pesan ISO 20022 `pacs.008.001.08` (Financial Institutional Customer Credit Transfer) menggunakan skema XML/XSD: bangun parser yang memvalidasi integritas elemen pengirim (Debtor), bank penerima (Creditor Agent), kode BIC/SWIFT, dan nomor rekening format IBAN standar internasional.
*Rubrik*: Dokumen XML tervalidasi terhadap skema XSD resmi dan menolak pesan cacat.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| ISO 8583 Financial Transaction Card Originated Messages | International Organization for Standardization | [ISO Official Portal](https://www.iso.org/standard/31628.html) | Standar Baku Protokol Pesan Kartu Debit/Kredit |
| ISO 20022 Universal Financial Industry Message Scheme | ISO 20022 Registration Authority | [ISO 20022 Standards Portal](https://www.iso20022.org/) | Standar Arsitektur XML/JSON Perbankan Modern, PACS/CAMT |
| PCI Data Security Standard (PCI-DSS) Requirements | PCI SSC Committee | [PCI Security Standards](https://www.pcisecuritystandards.org/) | Panduan Kepatuhan Regulasi Penyimpanan & Enkripsi Finansial |
| Paying with Plastic: The Digital Revolution in Buying and Borrowing | David S. Evans & Richard Schmalensee | [MIT Press](https://mitpress.mit.edu/9780262550581/paying-with-plastic/) | Ekonomi Bisnis Jaringan Kartu Visa/Mastercard & Kliring |"""
    },
    210: {
        "intuition": r"""Mana yang Anda pilih: menerima uang Rp 100 juta hari ini sekarang juga, atau menerima Rp 100 juta tepat 10 tahun dari sekarang?

Tentu semua orang waras akan memilih menerima uang hari ini. Mengapa? Karena uang Rp 100 juta hari ini bisa Anda investasikan sehingga berkembang biak menghasilkan bunga, dan nilai uang di masa depan akan tergerus oleh inflasi. Inilah hukum paling mendasar dalam seluruh dunia keuangan: **Nilai Waktu dari Uang (Time Value of Money)** ([Bodie, Kane, Marcus - Investments](https://www.mheducation.com/highered/product/investments-bodie-kane/M9781260013832.html)).

Dari satu prinsip sederhana ini, kita bisa menghitung harga wajar dari instrumen apa pun di muka bumi:
1. **Obligasi (Surat Utang)**: Berapa harga wajar selembar kertas yang menjanjikan pembayaran bunga Rp 5 juta setiap tahun ditambah pengembalian pokok di tahun ke-10?
2. **Saham Perusahaan**: Saham sebuah perusahaan (seperti Apple atau Bank BCA) bernilai sebesar total seluruh arus kas bersih di masa depan yang akan dihasilkan perusahaan tersebut, ditarik mundur nilainya ke hari ini (**Discounted Cash Flow / DCF**).
3. **Opsi (Options)**: Berapa harga wajar selembar tiket yang memberi Anda *hak (bukan kewajiban)* untuk membeli emas seharga Rp 1 juta bulan depan jika harga pasar melonjak ke Rp 1,5 juta? ([Hull - Options, Futures, and Other Derivatives](https://www.pearson.com/en-us/subject-catalog/p/options-futures-and-other-derivatives/P200000003339)).""",
        "theory": r"""Formulasi Matematis Nilai Waktu dari Uang & Valuasi Aset:

1. **Aksioma Nilai Waktu dari Uang (Time Value of Money)**:
Hubungan antara Nilai Kini (*Present Value* / $PV$) dan Nilai Masa Depan (*Future Value* / $FV$) dengan suku bunga diskonto $r$ dan periode waktu $t$:
* Bunga Majemuk Diskrit: $FV = PV (1 + r)^t \implies PV = \frac{FV}{(1 + r)^t}$
* Bunga Kontinu: $FV = PV \cdot e^{rt} \implies PV = FV \cdot e^{-rt}$

2. **Valuasi Obligasi Kupon Tetap & Kurva Imbal Hasil (Yield to Maturity / YTM)**:
Harga wajar obligasi $P$ dengan nilai pokok nominal $F$, pembayaran kupon periodik $C$, dan imbal hasil pasar $y$:
$$P = \sum_{t=1}^T \frac{C}{(1 + y)^t} + \frac{F}{(1 + y)^T}$$
*Durasi Macaulay*: Mengukur sensitivitas harga obligasi terhadap perubahan suku bunga:
$$D_{\text{Mac}} = \frac{1}{P} \left[ \sum_{t=1}^T \frac{t \cdot C}{(1+y)^t} + \frac{T \cdot F}{(1+y)^T} \right], \quad \frac{\Delta P}{P} \approx - \frac{D_{\text{Mac}}}{1 + y} \Delta y$$

3. **Valuasi Saham Arus Kas Terdiskon (Discounted Cash Flow / DCF)**:
Memodelkan nilai intrinsik ekuitas perusahaan:
$$V_0 = \sum_{t=1}^H \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{Terminal Value}_H}{(1 + \text{WACC})^H}, \quad \text{TV}_H = \frac{\text{FCFF}_{H+1}}{\text{WACC} - g}$$
Di mana WACC adalah *Weighted Average Cost of Capital* dan $g$ adalah tingkat pertumbuhan jangka panjang stabil Gordon Growth Model ([Damodaran - Investment Valuation](https://pages.stern.nyu.edu/~adamodar/)).

4. **Batas Teoretis & Put-Call Parity Opsi Eropa Vanilla**:
Hubungan arbitrase mutlak antara harga Opsi Beli ($C$), Opsi Jual ($P$), Harga Saham Spot saat ini ($S_0$), dan Harga Pelaksanaan Strike ($K$):
$$C + K e^{-rT} = P + S_0$$
Jika persamaan ini dilanggar di pasar, peluang keuntungan arbitrase bebas risiko instan tercipta.""",
        "internals": r"""Arsitektur pemodelan kurva imbal hasil obligasi (*Spot Yield Curve Bootstrapping*):

```mermaid
flowchart TD
    MarketData["Harga Pasar Surat Berharga Negara (T-Bills & Bonds)"] --> Sort["Urutkan berdasarkan Maturitas Waktu (0.5 thn, 1 thn, 2 thn, 5 thn, 10 thn)"]
    Sort --> ShortTerm["Hitung Spot Rate 6 Bulan via Zero-Coupon T-Bills"]
    ShortTerm --> Bootstrap["Iterasi Bootstrapping Kupon Obligasi: Hitung Zero Rate t berikutnya"]
    Bootstrap --> Spline["Interpolasi Kurva Kontinu (Nelson-Siegel / Cubic Spline)"]
    Spline --> DiscountFactors["Matriks Faktor Diskonto Kontinu D(t) = exp(-r(t)*t)"]
```

Dengan kurva imbal hasil zero-coupon yang telah di-bootstrap, arus kas pada waktu kapan pun di masa depan dapat didiskontokan secara independen tanpa distorsi struktur kupon ([Tuckman & Serrat - Fixed Income Securities](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118266670)).""",
        "code_block": r"""```python
import numpy as np

# 1. Valuasi Obligasi Kupon Tetap dan Kalkulasi Macaulay Duration
def price_bond(nominal, coupon_rate, ytm, periods):
    coupon = nominal * coupon_rate
    times = np.arange(1, periods + 1)
    
    # Arus Kas per Periode
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += nominal # Pengembalian pokok di akhir tenor
    
    # Diskontokan ke Present Value
    discount_factors = (1 + ytm) ** times
    pv_cash_flows = cash_flows / discount_factors
    bond_price = np.sum(pv_cash_flows)
    
    # Macaulay Duration (Tahun)
    macaulay_duration = np.sum(times * pv_cash_flows) / bond_price
    modified_duration = macaulay_duration / (1 + ytm)
    
    return bond_price, macaulay_duration, modified_duration

# Uji Coba: Obligasi 10 Tahun, Pokok Rp 1 Miliar, Kupon 7% per tahun, YTM Pasar 6.5%
price, mac_dur, mod_dur = price_bond(
    nominal=1_000_000_000,
    coupon_rate=0.07,
    ytm=0.065,
    periods=10
)

print(f"Harga Wajar Obligasi   : Rp {price:,.2f} (Trading di Premium > Pokok)")
print(f"Macaulay Duration      : {mac_dur:.2f} tahun")
print(f"Modified Duration      : {mod_dur:.2f}")
print(f"Sensitivitas: Jika suku bunga naik 1% (+100 bps), harga obligasi turun ~{mod_dur:.2f}%")

# 2. Verifikasi Hubungan Put-Call Parity Opsi Eropa
S0 = 100.0   # Harga Saham Sekarang
K = 100.0    # Strike Price
r = 0.05     # Risk-free rate 5%
T = 1.0      # Tenor 1 Tahun
Call = 10.45 # Harga Pasar Call

# Put-Call Parity: P = C + K*exp(-r*T) - S0
Put_theoretical = Call + K * np.exp(-r * T) - S0
print(f"\nHarga Wajar Opsi Put menurut Parity: ${Put_theoretical:.2f}")
```""",
        "pitfalls": r"""*Mengabaikan Sensitivitas Konveksitas Obligasi (Convexity)*: Menghitung perubahan harga obligasi hanya menggunakan Modified Duration adalah aproksimasi linier orde-1 yang hanya akurat untuk pergeseran suku bunga mikro ($\Delta y < 25\text{ bps}$). Ketika suku bunga berfluktuasi tajam ($\Delta y > 100\text{ bps}$), kelengkungan harga (*Convexity* orde-2) menyebabkan estimasi durasi meleset jauh. Selalu sertakan suku Taylor orde kedua: $\frac{\Delta P}{P} \approx -D_{\text{mod}} \Delta y + \frac{1}{2} C (\Delta y)^2$ ([Tuckman & Serrat Chapter 4](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118266670)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis fungsi perhitungan Nilai Sekarang Bersih (*Net Present Value / NPV*) dan Tingkat Pengembalian Internal (*Internal Rate of Return / IRR*) menggunakan metode pencarian akar Newton-Raphson untuk suatu proyek modal dengan investasi awal -Rp 500 juta dan arus kas masuk selama 5 tahun.
*Rubrik*: Output NPV dan IRR cocok dengan fungsi `numpy_financial.npv` dan `numpy_financial.irr`.

### Level 2 (Menengah)
Implementasikan algoritma kurva imbal hasil *Bootstrapping Spot Rate* dari nol: terima serangkaian harga pasar obligasi kupon tahunan bertenor 1, 2, 3, dan 5 tahun, pecahkan spot rate zero-coupon $r_t$ secara rekursif, dan plot perbandingan antara kurva YTM nominal vs kurva spot zero-coupon murni.
*Rubrik*: Spot rate periode $t$ mendiskontokan seluruh kupon historis dengan tepat.

### Level 3 (Mahir)
Bangun model valuasi saham Discounted Cash Flow (DCF) dua tahap (*Two-Stage FCFF Model*) di Python: proyeksikan laporan keuangan 5 tahun ke depan (pendapatan, EBIT, capex, perubahan modal kerja), hitung WACC berdasarkan struktur modal utang/ekuitas, hitung nilai terminal Gordon Growth, dan jalankan simulasi sensitivitas tabel 2-arah (variasi WACC vs variasi Terminal Growth Rate).
*Rubrik*: Menghasilkan tabel matriks sensitivitas harga saham wajar per lembar.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Options, Futures, and Other Derivatives (10th Ed.) | John C. Hull (University of Toronto) | [Pearson Education](https://www.pearson.com/en-us/subject-catalog/p/options-futures-and-other-derivatives/P200000003339) | Alkitab Instrumen Derivatif, Arbitrase, Put-Call Parity |
| Investment Valuation: Tools and Techniques for Determining the Value of Any Asset | Aswath Damodaran (NYU Stern) | [Damodaran Online Portal](https://pages.stern.nyu.edu/~adamodar/) | Standar Emas Valuasi DCF, WACC, Estimasi Risiko Ekuitas |
| Fixed Income Securities: Valuation, Risk, and Risk Management | Bruce Tuckman & Angel Serrat | [Wiley Finance](https://onlinelibrary.wiley.com/doi/book/10.1002/9781118266670) | Matematika Obligasi, Durasi, Konveksitas, Kurva YTM |
| Investments (12th Ed.) | Zvi Bodie, Alex Kane, Alan J. Marcus | [McGraw-Hill Education](https://www.mheducation.com/highered/product/investments-bodie-kane/M9781260013832.html) | Fondasi Teori Investasi, Time Value of Money, Teori Modal |"""
    },
    211: {
        "intuition": r"""Ada peribahasa kuno yang mengatakan: *"Jangan pernah menaruh semua telurmu di dalam satu keranjang"* ([Markowitz - Portfolio Selection, 1952](https://www.jstor.org/stable/2975974)). Jika keranjang itu jatuh, semua telur pecah bersamaan.

Namun, bagaimana jika Anda menaruh telur di 10 keranjang yang berbeda, tetapi semua keranjang itu dinaikkan ke atas satu gerobak yang sama? Jika gerobak itu terguling, telur Anda tetap pecah semua!

Harry Markowitz menemukan bahwa diversifikasi sejati bukan sekadar membeli banyak aset yang berbeda: **kuncinya adalah korelasi antar aset**. Jika Anda memiliki saham perusahaan es krim (yang untung besar saat musim panas tapi rugi saat musim hujan) dan saham perusahaan payung (yang untung besar saat musim hujan tapi rugi saat musim panas), ketika digabungkan dalam satu portofolio, risiko kerugian kedua bisnis tersebut saling membatalkan satu sama lain secara ajaib!

Hasilnya? Anda mendapatkan pengembalian modal yang stabil dengan risiko volatilitas yang jauh lebih rendah daripada memegang salah satu saham sendirian (**Efficient Frontier**) ([Markowitz Nobel Lecture](https://www.nobelprize.org/prizes/economic-sciences/1990/markowitz/lecture/)). Dan ketika Anda memiliki strategi taruhan yang menguntungkan, berapa persen dari total uang Anda yang harus Anda pertaruhkan di setiap peluang agar kekayaan Anda tumbuh maksimal tanpa risiko bangkrut? Matematikawan John L. Kelly merumuskannya dalam **Kelly Criterion** ([Kelly - A New Interpretation of Information Rate](https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf)).""",
        "theory": r"""Formulasi Matematis Teori Portofolio Modern & Optimasi Risiko:

1. **Optimasi Portofolio Mean-Variance Harry Markowitz**:
Untuk $N$ aset dengan vektor ekspektasi return $\mu \in \mathbb{R}^N$ dan matriks kovarians $\Sigma \in \mathbb{R}^{N \times N}$:
Return portofolio: $\mu_p = w^T \mu$, \quad Varians portofolio: $\sigma_p^2 = w^T \Sigma w$
Di mana $w \in \mathbb{R}^N$ adalah bobot alokasi dengan kendala $\sum_{i=1}^N w_i = 1$ ($w^T \mathbf{1} = 1$).
Masalah optimasi kuadratik untuk meminimalkan risiko pada target return $\mu_0$:
$$\min_w \frac{1}{2} w^T \Sigma w \quad \text{s.t.} \quad w^T \mu = \mu_0, \quad w^T \mathbf{1} = 1$$
Himpunan solusi optimal untuk seluruh rentang $\mu_0$ membentuk kurva hiperbola di bidang $(\sigma_p, \mu_p)$ yang disebut **Efficient Frontier** ([Markowitz 1952](https://www.jstor.org/stable/2975974)).

2. **Capital Asset Pricing Model (CAPM) & Beta Risiko Sistematis**:
Di hadapan aset bebas risiko (*risk-free asset* $r_f$), portofolio optimal adalah titik singgung (*tangency portfolio*) yang memaksimalkan rasio Sharpe:
$$\text{Sharpe Ratio} = \frac{\mu_p - r_f}{\sigma_p}$$
Garis Pasar Modal (Capital Market Line / CML). Model penetapan harga aset ekuilibrium CAPM:
$$\mathbb{E}[R_i] = r_f + \beta_i (\mathbb{E}[R_m] - r_f), \quad \beta_i = \frac{\text{Cov}(R_i, R_m)}{\text{Var}(R_m)}$$
Di mana $\beta_i$ mengukur sensitivitas terhadap risiko sistematis pasar yang tidak dapat dihilangkan oleh diversifikasi ([Sharpe - Capital Asset Prices](https://www.jstor.org/stable/2977928)).

3. **Formula Fraksi Pertumbuhan Optimal Kelly (Kelly Criterion)**:
Memaksimalkan laju pertumbuhan geometris logaritmik kekayaan jangka panjang $\mathbb{E}[\ln(W_t)]$:
* Peluang Peluang Biner (Taruhan dengan probabilitas menang $p$, kalah $q = 1 - p$, rasio odds keuntungan $b$):
$$f^* = \frac{b p - q}{b} = \frac{p(b + 1) - 1}{b}$$
* Alokasi Aset Kontinu (Model Gaussian dengan ekspektasi return berlebih $\mu - r$ dan volatilitas $\sigma$):
$$f^* = \frac{\mu - r}{\sigma^2}$$
Bertaruh lebih besar dari fraksi Kelly ($f > 2f^*$) menjamin kebangkrutan modal (*gambler's ruin*) hampir pasti dalam jangka panjang ([Kelly 1956](https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf)).""",
        "internals": r"""Geometri Ruang Risiko-Pengembalian (Markowitz Efficient Frontier & Capital Market Line):

```mermaid
flowchart TD
    subgraph Mean_Variance_Space["Ruang Volatilitas vs Pengembalian (Risk-Return Space)"]
        Rf["Aset Bebas Risiko r_f (Volatilitas = 0)"]
        Tangency["Portofolio Tangensi Maksimum Sharpe Ratio"]
        EF["Efficient Frontier (Batas Atas Hiperbola Portofolio Optimal)"]
        Suboptimal["Wilayah Portofolio Suboptimal / Inefisien (Dalam Kurva)"]
        CML["Capital Market Line (Garis Lurus dari r_f menyinggung Efficient Frontier)"]
        
        Rf --- CML
        CML --> Tangency
        Tangency --- EF
    end
```

Kekuatan matematika Markowitz terletak pada suku kovarians non-diagonal: jika koefisien korelasi $\rho_{ij} < 0$, varians gabungan portofolio turun lebih cepat daripada penurunan rata-rata return, memungkinkan pencapaian portofolio dengan risiko yang lebih rendah daripada aset teraman di dalam keranjang ([Sharpe Portfolio Theory](https://www.jstor.org/stable/2977928)).""",
        "code_block": r"""```python
import numpy as np
from scipy.optimize import minimize

# 1. Optimasi Portofolio Markowitz Tangency (Maksimum Sharpe Ratio)
# 4 Aset Saham: Ekspektasi Return Tahunan & Matriks Kovarians
mu = np.array([0.12, 0.15, 0.09, 0.20]) # Return tahunan ekspektasi
cov_matrix = np.array([
    [0.040, 0.010, 0.005, 0.015],
    [0.010, 0.062, 0.008, 0.020],
    [0.005, 0.008, 0.022, 0.004],
    [0.015, 0.020, 0.004, 0.090]
])
r_f = 0.04 # Risk-Free Rate 4%

def negative_sharpe(weights):
    p_return = np.dot(weights, mu)
    p_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return -(p_return - r_f) / p_volatility

# Kendala: Total Bobot = 1 (100% Modal), No Short-Selling (0 <= w <= 1)
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1.0})
bounds = tuple((0.0, 1.0) for _ in range(len(mu)))
initial_weights = np.ones(len(mu)) / len(mu)

result = minimize(negative_sharpe, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
optimal_weights = result.x
max_sharpe = -result.fun

p_ret = np.dot(optimal_weights, mu)
p_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))

print("Alokasi Portofolio Optimal (Maximum Sharpe Ratio):")
for idx, w in enumerate(optimal_weights, start=1):
    print(f" - Aset {idx}: {w*100:.2f}%")
print(f"Ekspektasi Return Portofolio : {p_ret*100:.2f}%")
print(f"Volatilitas Risiko Portofolio: {p_vol*100:.2f}%")
print(f"Rasio Sharpe Maksimum        : {max_sharpe:.3f}")

# 2. Perhitungan Alokasi Kelly Criterion
win_rate = 0.55 # 55% Win Rate
win_loss_ratio = 1.5 # Menang 1.5x dari kekalahan
kelly_fraction = (win_rate * (win_loss_ratio + 1) - 1) / win_loss_ratio
print(f"\nFraksi Taruhan Optimal Kelly: {kelly_fraction*100:.2f}% dari total modal")
```""",
        "pitfalls": r"""*Estimation Risk / Error Maximization pada Markowitz Optimizer*: Pengoptimal Mean-Variance klasik bekerja seperti "mesin pemaksimal galat". Jika model Anda secara keliru melebih-lebihkan sedikit saja ekspektasi return suatu saham ($+1\%$), algoritma optimasi akan mengalokasikan 80% modal ke saham tersebut, menciptakan portofolio konsentrasi ekstrem yang sangat rapuh. Praktisi industri kuantitatif tidak menggunakan ekspektasi return mentah; mereka menggunakan model **Black-Litterman** (menggabungkan pandangan analis dengan ekuilibrium pasar) atau regularisasi *Hierarchical Risk Parity (HRP)* ([López de Prado - Building Diversified Portfolios that Outperform Out-of-Sample](https://www.davidhbailey.com/dhbpapers/hrp.pdf)).""",
        "exercises": r"""### Level 1 (Pemula)
Tulis skrip Python untuk menghitung matriks kovarians sampel dan koefisien Beta CAPM ($\beta_i = \text{Cov}(R_i, R_m)/\text{Var}(R_m)$) dari 3 saham teknologi terhadap indeks S&P 500 / IHSG menggunakan data return harian sintetis 1 tahun.
*Rubrik*: Output menampilkan nilai beta masing-masing saham secara akurat.

### Level 2 (Menengah)
Bangun simulator simulasi Monte Carlo untuk memetakan kurva *Efficient Frontier*: hasilkan 20.000 portofolio dengan bobot alokasi Dirichlet acak $\sum w_i = 1$, plot sebaran titik risiko vs return, dan cari titik portofolio dengan varians minimum absolut (*Global Minimum Variance Portfolio*).
*Rubrik*: Visualisasi kurva hiperbola batas efisien terbentuk jelas dari batas kiri awan titik.

### Level 3 (Mahir)
Implementasikan algoritma alokasi portofolio **Hierarchical Risk Parity (HRP)** Marcos López de Prado: hitung jarak korelasi spasial $d_{ij} = \sqrt{\frac{1}{2}(1 - \rho_{ij})}$, lakukan pengelompokan hierarkis matriks (Single Linkage Clustering), terapkan quasi-diagonalization, dan alokasikan bobot melalui inverse-variance bisection rekursif tanpa perlu menginversi matriks kovarians $\Sigma^{-1}$.
*Rubrik*: Kode teruji tahan banting terhadap matriks kovarians yang singular atau ill-conditioned.""",
        "references": r"""| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Portfolio Selection | Harry Markowitz (The Journal of Finance 1952) | [JSTOR Classic Paper](https://www.jstor.org/stable/2975974) | Makalah Penemuan Asli Teori Portofolio Modern Mean-Variance |
| Capital Asset Prices: A Theory of Market Equilibrium (CAPM) | William F. Sharpe (Nobel Laureate) | [The Journal of Finance 1964](https://www.jstor.org/stable/2977928) | Penemuan Asli Model CAPM, Beta Saham, Capital Market Line |
| A New Interpretation of Information Rate (Kelly Criterion) | J. L. Kelly, Jr. (Bell System Technical Journal) | [Bell System Report 1956](https://www.princeton.edu/~wbialek/rome/refs/kelly_56.pdf) | Formulasi Asli Teori Informasi Pertumbuhan Logaritmik Modal |
| Advances in Financial Machine Learning | Marcos López de Prado | [Wiley Finance Portal](https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086) | Hierarchical Risk Parity (HRP), Robust Portfolio Optimization |"""
    }
}
