# Modul 216: Arsitektur Blockchain, Smart Contracts & DeFi (Struktur Merkle Trees, Model UTXO vs Akun, Konsensus PoW/PoS, EVM, AMM Uniswap)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 14: Tingkat 14: Fintech, Financial Engineering, HFT & Blockchain](./README.md)
*Sebelumnya*: [215. rekayasa-sistem-berlatensi-ultra-rendah-hft](./215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md) | *Berikutnya*: [217. sistem-mekatronika-transmisi-mekanis](../15-mekatronika-robotika-kendali/217-sistem-mekatronika-transmisi-mekanis.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Bagaimana sekelompok orang asing di seluruh dunia yang tidak saling mengenal dan tidak saling mempercayai bisa bersama-sama menyepakati satu buku besar keuangan tunggal tanpa ada bank, presiden, polisi, atau server pusat yang mengaturnya?

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Satoshi Nakamoto memecahkan teka-teki legendaris ilmu komputer ini (**Masalah Para Jenderal Bizantium / Byzantine Generals Problem**) melalui penemuan **Blockchain & Konsensus Proof-of-Work (PoW)** ([Nakamoto - Bitcoin: A Peer-to-Peer Electronic Cash System](https://bitcoin.org/bitcoin.pdf)).

Bayangkan sebuah buku kas raksasa di mana setiap halaman buku (*blok*) berisi daftar ratusan transaksi keuangan. Untuk mengunci halaman tersebut agar tidak ada yang bisa memalsukannya:
1. Halaman tersebut dirangkum menggunakan rumus matematika sidik jari digital (**Pohon Merkle / Merkle Tree**) ([Merkle - A Certified Digital Signature](https://link.springer.com/chapter/10.1007/0-387-34799-2_32)).
2. Halaman baru harus mencantumkan sidik jari dari halaman sebelumnya, membentuk **Rantai Blok (Blockchain)**.
3. Para penambang (*miners*) harus menghabiskan miliaran daya listrik untuk memecahkan teka-teki kriptografi yang sangat sulit (*Proof-of-Work*) agar halaman mereka disetujui.

Vitalik Buterin kemudian memperluas ide ini menjadi **Ethereum Virtual Machine (EVM)**: tidak hanya mencatat angka transfer uang, blockchain bisa menjalankan kode program komputer abadi yang tidak bisa dimatikan oleh siapa pun (**Smart Contracts & DeFi**) ([Buterin - Ethereum Whitepaper](https://ethereum.org/en/whitepaper/)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Formulasi Kriptografi Blockchain & Keuangan Terdesentralisasi:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
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
Harga marginal spot: $P = \frac{y}{x}$, dengan *Slippage* yang tumbuh proporsional terhadap ukuran pertukaran $\frac{\Delta x}{x}$.

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur State Transition Function pada Ethereum Virtual Machine (EVM):

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

EVM beroperasi sebagai mesin status Turing-Complete kuasi-deterministik: setiap instruksi komputasi mengenakan biaya bahan bakar (*Gas*) yang harus dibayar pengirim, menyelesaikan masalah *Halting Problem* secara elegan (program dengan infinite loop akan mati kehabisan gas secara otomatis) ([Wood - Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf)).

#### Tabel Penelusuran Eksploitasi Reentrancy Kontrak Pintar The DAO di Jaringan Ethereum
| Timestamp / Sequence ID | Komponen / Lapisan Sistem | Pesan Masuk (FIX / Transaksi) | Operasi Antrean / Komputasi Buku | State Buku Pesanan (LOB / Ledger) | Event Terpancar (Fill / Block Emit) |
|---|---|---|---|---|---|
| 17 Jun 2016 (Blok #1718497) | Smart Contract The DAO | Transaksi Penarikan Dana Penyerang | Penyerang memanggil fungsi `withdrawRewardFor()` | Saldo Ether The DAO: 12 Juta ETH (\$150 Miliar) | Penyerang menyiapkan kontrak penyerang eksploit |
| Pemanggilan Eksternal Cacat | Eksekusi EVM Opcode `CALL` | DAO mengirim dana via `msg.sender.call.value()` | Eksekusi berpindah ke kontrak penyerang SEBELUM saldo di-nolkan! | Saldo penyerang di memori state DAO masih tercatat penuh | Pelanggaran pola Checks-Effects-Interactions! |
| Pemanggilan Ulang Rekursif | Fungsi Fallback Kontrak Penyerang | Kontrak penyerang memanggil kembali `withdrawRewardFor()` | EVM mengeksekusi reentrant call; saldo dicek kembali dan masih ada! | DAO mengirim transfer dana kedua kalinya! | Loop reentrancy bersarang menguras brankas kontrak |
| 30 Iterasi Rekursi Per Blok | Mesin Virtual Ethereum (EVM) | Pengurasan saldo tanpa mendebit catatan buku besar | Saldo internal baru didebit setelah seluruh pemanggilan selesai | Saldo penyerang akhirnya di-nolkan, tapi uang sudah lenyap! | Penyerang menguras 3,6 Juta Ether (\$60 Juta) |
| Garpu Keras (Hard Fork) | Komunitas Pengembang Ethereum | Proposal Pemulihan Dana Korban | Rollback keadaan rantai blok melalui Hard Fork darurat | Rantai blok terbelah dua: Ethereum (ETH) & Ethereum Classic (ETC) | Peristiwa pemisahan konsensus blockchain paling dramatis! |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
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
```

## 5. Miskonsepsi & Jebakan Industri
*Kerentanan Serangan Reentrancy pada Smart Contract (Bencana The DAO)*: Dalam kode Solidity, jika kontrak mentransfer koin ether ke alamat pengguna eksternal sebelum memperbarui catatan saldo internalnya (`msg.sender.call{value: amount}("")`), kontrak penerima yang jahat dapat menulis fungsi fallback yang memanggil kembali fungsi penarikan tersebut (*re-entrant call*) secara rekursif sebelum saldo berkurang, menguras seluruh dana kas kontrak. Selalu terapkan pola desain **Checks-Effects-Interactions** atau gunakan ReentrancyGuard mutex ([Atzei et al. - A Survey of Attacks on Ethereum Smart Contracts](https://link.springer.com/chapter/10.1007/978-3-662-54455-6_8)).

### Studi Kasus Kegagalan Nyata: Eksploitasi Serangan Reentrancy Smart Contract The DAO ($60 Juta Ether Drained, Juni 2016)
- **Kronologi & Konteks Sejarah**: Pada tanggal 17 Juni 2016, sebuah organisasi otonom terdesentralisasi perintis di jaringan Ethereum, *The DAO*—yang berhasil mengumpulkan 14% dari seluruh sirkulasi Ether di dunia (senilai $150 Juta pada saat itu)—dibobol oleh peretas tak dikenal yang berhasil menyedot lebih dari 3,6 Juta ETH (senilai $60 Juta) ke dalam sebuah kontrak *Dark DAO* anak. Skandal eksploitasi ini memicu perdebatan moral filosofis dan teknis yang sengit di komunitas blockchain global hingga berujung pada keputusan kontroversial pelaksanaan *Hard Fork* darurat yang membelah blockchain menjadi dua rantai terpisah: **Ethereum (ETH)** dan **Ethereum Classic (ETC)**.
- **Akar Masalah Rekayasa Smart Contract & Pelanggaran Pola Checks-Effects-Interactions**: Kerentanan The DAO terletak pada urutan logika eksekusi fungsi penarikan dana reward (*withdraw*). Kontrak pintar mentransfer dana mata uang Ether ke alamat pemanggil menggunakan instruksi tingkat rendah `msg.sender.call.value(amount)()` *sebelum* mengurangi saldo internal akun pemanggil (`balances[msg.sender] = 0`). Dalam arsitektur Ethereum Virtual Machine (EVM), ketika pemanggilan eksternal mentransfer Ether ke alamat kontrak lain, kontrol eksekusi CPU EVM diserahkan sepenuhnya ke fungsi penerima bawaan (*Fallback / Receive Function*) dari kontrak penerima tersebut. Penyerang menyusun kontrak berbahaya yang di dalam fungsi fallback-nya memanggil ulang (*re-enter*) fungsi penarikan dana DAO secara rekursif. Karena status saldo internal belum sempat diperbarui, pemeriksaan kondisi saldo (`require(balances[msg.sender] > 0)`) selalu lolos, memungkinkan penyerang menguras saldo kas brankas DAO puluhan kali lipat dalam satu transaksi tunggal.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// REKONSTRUKSI CACAT KONTRAK THE DAO (Reentrancy Vulnerability)
contract VulnerableDAOBank {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // FUNGSI CACAT ASLI: Mentransfer dana SEBELUM memperbarui state saldo!
    function withdrawAllFunds() external {
        uint256 balance = balances[msg.sender];
        require(balance > 0, "Saldo tidak mencukupi");

        // 1. PANGGILAN EKSTERNAL KE ALAMAT PENYERANG:
        // Kontrol eksekusi EVM berpindah ke kontrak penyerang!
        (bool success, ) = msg.sender.call{value: balance}("");
        require(success, "Transfer gagal");

        // 2. PEMBARUAN STATE TERLAMBAT (CACAT FATAL):
        // Baris ini TIDAK PERNAH TERCAPAI karena penyerang memanggil ulang fungsi di atas!
        balances[msg.sender] = 0;
    }
}

// MITIGASI RESMI: Pola Checks-Effects-Interactions & Mutex ReentrancyGuard
abstract contract ReentrancyGuard {
    uint256 private _status = 1; // 1: NOT_ENTERED, 2: ENTERED
    modifier nonReentrant() {
        require(_status != 2, "REENTRANCY_DETECTED: Panggilan berulang ditolak!");
        _status = 2; // Kunci mutex
        _;
        _status = 1; // Lepas kunci
    }
}

contract SecureDAOBank is ReentrancyGuard {
    mapping(address => uint256) public balances;

    function withdrawSecure() external nonReentrant {
        // 1. CHECKS: Validasi kondisi
        uint256 amount = balances[msg.sender];
        require(amount > 0, "Saldo kosong");

        // 2. EFFECTS: Mutasi state internal terlebih dahulu SEBELUM interaksi eksternal!
        balances[msg.sender] = 0;

        // 3. INTERACTIONS: Transfer dana dilakukan paling akhir
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer gagal");
    }
}
```

- **Analisis Forensik & Rekayasa Modern**: Tragedi The DAO menjadi fondasi standar rekayasa perangkat lunak keamanan smart contract: (1) Penerapan wajib pola desain **Checks-Effects-Interactions (CEI)** di mana pembaruan variabel state internal wajib diselesaikan sebelum melakukan transfer dana atau pemanggilan eksternal; (2) Penggunaan pengunci mutex bawaan teruji seperti modul OpenZeppelin **`ReentrancyGuard` (`nonReentrant` modifier)**; (3) Integrasi alat analisis statis dan deteksi simbolik bytecode otomatis (**Slither, Mythril, Securify**) dalam pipeline CI/CD sebelum deployment kontrak ke mainnet; (4) Menghindari pemanggilan eksternal raw `.call.value()` yang meneruskan seluruh gas, dan menggantinya dengan pola penarikan berbasis pull (*Pull-over-Push Payment Pattern*).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Tulis simulasi algoritma penambangan konsensus Proof-of-Work (PoW) sederhana di Python: terima data string blok, lakukan hashing berulang dengan incrementing nonce hingga menemukan hash SHA-256 yang diawali oleh 4 karakter nol ("0000"), dan catat total iterasi serta waktu komputasi yang dibutuhkan.
*Rubrik*: Output mencetak nonce pemenang dan hash valid yang memenuhi target kesulitan.

### Level 2 (Menengah)
Implementasikan struktur Pohon Merkle lengkap beserta fungsi pembuatan bukti audit (*Merkle Proof Generator*) dan verifikasi bukti (*Merkle Proof Verifier*): buktikan bahwa simpul daun dapat divalidasi keabsahannya terhadap Merkle Root hanya menggunakan deretan hash tetangga tanpa mengetahui isi daun lainnya.
*Rubrik*: Fungsi verifikator mengembalikan `True` untuk bukti yang sah dan `False` jika data dipalsukan.

### Level 3 (Mahir)
Bangun smart contract Automated Market Maker (AMM) Uniswap v2 mini menggunakan bahasa Solidity atau simulator komputasional Python lengkap: implementasikan fungsi penambahan likuiditas (`mint` LP Token berbasis $\sqrt{x \cdot y}$), fungsi penghapusan likuiditas (`burn`), dan fungsi pertukaran (`swap`) dengan proteksi reentrancy lock.
*Rubrik*: Invarian produk konstan terverifikasi meningkat secara monotonik akibat akumulasi fee transaksi.

### Tingkat 1: Dasar
- **Tugas**: Tulis kontrak pintar Solidity mini (`Vault.sol`) yang menerima deposit Ether dan mengimplementasikan fungsi penarikan dana yang aman dari serangan Reentrancy dengan mematuhi pola desain Checks-Effects-Interactions (CEI) secara ketat.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan saldo pengguna dalam `mapping(address => uint256) public balances`.
  - Pada fungsi `withdraw(uint256 amount)`: (1) `require(balances[msg.sender] >= amount)`; (2) Kurangkan saldo: `balances[msg.sender] -= amount`; (3) Kirim Ether: `(bool sent, ) = msg.sender.call{value: amount}("")`.
  - Tulis tes unit pengujian yang membuktikan bahwa saldo akun terdebit dengan benar.
- **Test Vector & Kasus Uji**:
  - Pengguna mendepositokan 5 Ether, lalu menarik 2 Ether.
  - Saldo yang tercatat di pemetaan internal harus bernilai tepat 3 Ether, dan saldo dompet pengguna bertambah 2 Ether.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Kode Solidity valid, urutan pola CEI presisi, penanganan transfer aman.
  - Skor 50%: Menulis transfer sebelum pengurangan saldo tanpa pengunci mutex (rentan reentrancy).
  - Skor 0%: Menggunakan fungsi `send()` atau `transfer()` usang yang memiliki batasan gas 2300 tanpa penanganan status kegagalan.

### Tingkat 2: Menengah
- **Tugas**: Bangun kontrak pintar penyerang (*Attacker.sol*) dalam Solidity yang menyimulasikan eksploitasi Reentrancy terhadap kontrak bank yang rentan: Fungsi `attack()` menyetor 1 Ether, memicu fungsi penarikan pertama, dan di dalam fungsi `receive() external payable`, panggil ulang fungsi penarikan target hingga saldo brankas bank habis terkuras.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan alamat kontrak target yang rentan sebagai variabel state.
  - Pada fungsi `receive()`: Periksa apakah `address(target).balance >= 1 ether`. Jika ya, panggil kembali `target.withdraw()`.
  - Hentikan pemanggilan rekursif jika saldo target habis, lalu transfer seluruh Ether hasil curian ke dompet peretas.
- **Test Vector & Kasus Uji**:
  - Uji di lingkungan Foundry atau Hardhat lokal: Bank memiliki 10 Ether dari korban lain.
  - Penyerang mendepositokan 1 Ether dan mengeksekusi `attack()`: Saldo bank harus terkuras menjadi 0 Ether, dan saldo penyerang bertambah menjadi 11 Ether dalam 1 transaksi tunggal.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Eksploitasi reentrancy berhasil menguras saldo target secara deterministik, penanganan kondisi berhenti rekursi rapi.
  - Skor 50%: Reentrancy terpicu namun terjebak out-of-gas karena lupa menyetel kondisi penghenti pada fungsi receive.
  - Skor 0%: Kontrak penyerang tidak memiliki fungsi fallback/receive.

### Tingkat 3: Mahir
- **Tugas**: Rancang detektor kerentanan Reentrancy statis otomatis (*Static AST Reentrancy Scanner*) dalam Python yang membaca Abstract Syntax Tree (AST) berkas kontrak pintar Solidity (hasil ekspor `solc --ast-compact-json`): Pindai seluruh fungsi publik/eksternal, identifikasi apakah terdapat pemanggilan fungsi eksternal tingkat rendah (`call`, `transfer`, `send`) yang mendahului instruksi pembaruan variabel state penyimpanan (`Assignment` ke `StateVariable / IndexAccess`), dan laporkan potensi celah Reentrancy dengan nomor baris kode presisi.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun penelusuran graf aliran kontrol (*Control Flow Graph / CFG*) fungsi.
  - Tandai simpul AST: Simpul `ExternalCall` vs Simpul `StateMutation`.
  - Jika path eksekusi menemui simpul `ExternalCall` sebelum `StateMutation` pada fungsi yang tidak memiliki modifier `nonReentrant`, tandai sebagai `CRITICAL_REENTRANCY_VULNERABILITY`.
- **Test Vector & Kasus Uji**:
  - Masukkan AST kontrak rentan (The DAO): Scanner harus menandai baris panggilan eksternal sebagai kerentanan kritis.
  - Masukkan AST kontrak aman (dengan pola CEI atau modifier nonReentrant): Scanner harus menyatakan kontrak aman tanpa false positive.
- **Rubrik Penilaian Objektif**:
  - Skor 100%: Analisis AST presisi, deteksi pola urutan CEI akurat, verifikasi modifier nonReentrant tepat.
  - Skor 50%: Menggunakan pencarian string regex sederhana alih-alih inspeksi pohon sintaksis AST JSON.
  - Skor 0%: Gagal membedakan antara variabel lokal memori dan variabel state penyimpanan blockchain.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Bitcoin: A Peer-to-Peer Electronic Cash System | Satoshi Nakamoto | [Bitcoin Whitepaper PDF](https://bitcoin.org/bitcoin.pdf) | Makalah Penemuan Blockchain Asli, Proof-of-Work, Konsensus |
| Ethereum: A Next-Generation Smart Contract and Decentralized Application Platform | Vitalik Buterin | [Ethereum Whitepaper](https://ethereum.org/en/whitepaper/) | Konsep Mesin Virtual EVM, Smart Contracts, Gas Metering |
| Uniswap v2 Core Whitepaper | Hayden Adams, Noah Zinsmeister, Dan Robinson | [Uniswap Official Whitepaper](https://uniswap.org/whitepaper.pdf) | Matematika Constant Product Market Maker AMM, Invarian xy=k |
| Ethereum Yellow Paper: The Formal Specification of Ethereum | Gavin Wood (Polkadot Founder) | [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf) | Spesifikasi Matematis Formal Opcode EVM & Merkle Patricia Trie |

---
*Navigasi Cepat*: [Ke Tingkat 14](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [215. rekayasa-sistem-berlatensi-ultra-rendah-hft](./215-rekayasa-sistem-berlatensi-ultra-rendah-hft.md) | *Berikutnya*: [217. sistem-mekatronika-transmisi-mekanis](../15-mekatronika-robotika-kendali/217-sistem-mekatronika-transmisi-mekanis.md)
