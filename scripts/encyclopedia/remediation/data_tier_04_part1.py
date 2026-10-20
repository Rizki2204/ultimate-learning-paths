# -*- coding: utf-8 -*-
"""
Authentic Remediation Data for Tier 04 Part 1 (Topics 53-61):
Digital Logic, RTL Synthesis, FSMs & Hardware Memory.
"""

DATA_TIER_04_PART1 = {
    53: {
        "trace": r"""#### Tabel Penelusuran Glitch Bahaya Logika Statis (Static-1 Hazard) & Reset Asinkron Palsu
| Waktu Simulasi ($t$) | Transisi Vektor Input ($A, B, C$) | Output Gerbang AND 1 ($A \cdot B$) | Output Gerbang Inverter NOT ($\bar{B}$) | Output Gerbang AND 2 ($\bar{B} \cdot C$) | Sinyal Reset Gerbang OR ($Y = AB + \bar{B}C$) |
|---|---|---|---|---|---|
| $t = 0.0\text{ ns}$ | $A=1, B=1, C=1$ | $1 \cdot 1 = 1$ | $0$ (Terhambat delay gate) | $0 \cdot 1 = 0$ | $Y = 1 + 0 = 1$ (Sinyal Reset stabil HIGH) |
| $t = 1.0\text{ ns}$ | Input $B$ beralih: $1 \to 0$ | $1 \cdot 0 = 0$ (Jatuh instan) | Output masih $0$ ($t_{pd,inv} = 2\text{ns}$) | $0 \cdot 1 = 0$ | $Y = 0 + 0 = 0$ (GLITCH STATIS-1 ANJLOK LOW!)|
| $t = 2.0\text{ ns}$ | Delay perambatan inverter | $0$ | Output masih transisi | $0$ | Pulsa sempit glitch $0$ selebar $2\text{ ns}$ tercipta |
| $t = 3.0\text{ ns}$ | Inverter selesai berbalik | $0$ | Menjadi $1$ | $1 \cdot 1 = 1$ | $Y = 0 + 1 = 1$ (Kembali pulih ke HIGH) |
| Efek pada Flip-Flop | Pin Reset Active-Low terpicu | Glitch pulsa $2\text{ ns}$ melintasi ambang | Reset asinkron terpicu tanpa perintah! | Register status sistem kembali ke $0$ | Kontroler komunikasi satelit reboot mendadak |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Glitch Bahaya Logika Statis (Static-1 Hazard) Memicu Reset Asinkron Palsu Sistem Komunikasi",
            "chronology": r"""- **Insiden Kegagalan Pengontrol Antariksa**: Pada modul kontroler telemetri satelit cuaca geostasioner, prosesor pengendali mengalami reboot spontan berulang setiap kali register status beralih status internal tertentu. Kegagalan acak ini terjadi tanpa ada perintah reset eksternal dari stasiun bumi.
- **Akar Masalah Aljabar Boolean & Keterlambatan Gerbang Fisik**: Fungsi logika yang disederhanakan murni menggunakan minimisasi Karnaugh Map (K-Map) minimal $Y = AB + \bar{B}C$ rentan terhadap bahaya statis-1 (*static-1 hazard*). Ketika $A=1$ dan $C=1$, output secara teoritis harus selalu bernilai 1 independen terhadap nilai $B$ ($Y = 1\cdot B + \bar{B}\cdot 1 = B + \bar{B} = 1$). Namun di dunia silikon fisik, sinyal $B$ yang mengalir ke gerbang NOT membutuhkan waktu tunda propagasi ($t_{pd} \approx 2\text{ ns}$) untuk berbalik nilai. Saat $B$ beralih dari 1 ke 0, gerbang AND pertama padam seketika sebelum gerbang AND kedua sempat menyala. Selama jeda 2 nanodetik tersebut, kedua input gerbang OR bernilai 0, memuntahkan denyut glitch sempit $1 \to 0 \to 1$. Karena output ini terhubung ke pin reset asinkron active-low flip-flop, glitch tersebut langsung meng-clear status prosesor seketika.""",
            "snippet": r"""```verilog
// Modul Verilog Demonstrasi Glitch Hazard vs Redundant Cover Mitigasi
module hazard_demonstration (
    input  wire A, B, C,
    output wire Y_vulnerable,
    output wire Y_hazard_free
);
    // Rangkaian rentan Static-1 Hazard (minimisasi minimalis K-Map):
    // Ketika A=1, C=1 dan B beralih 1->0, glitch 0 sesaat tercipta
    wire not_B;
    assign #2 not_B = ~B; // Simulasi keterlambatan gerbang inverter 2ns
    wire term1 = A & B;
    wire term2 = not_B & C;
    assign Y_vulnerable = term1 | term2;

    // Rangkaian Hazard-Free (Menambahkan term redundan konsensus AC):
    // Term redundan (A & C) menahan output tetap 1 saat B sedang bertransisi
    wire term_redundant = A & C;
    assign Y_hazard_free = term1 | term2 | term_redundant;
endmodule
```""",
            "analysis": r"""- **Teorema Redundansi Konsensus Boolean**: Untuk mengeliminasi static-1 hazard, perancang dilarang menggunakan minimisasi ekspresi minimal K-Map telanjang. Setiap pasang *prime implicant* yang bertetangga pada K-Map wajib dihubungkan oleh prime implicant redundan penutup (*consensus term / hazard-free cover*, yaitu menyertakan $AC$ dalam $Y = AB + \bar{B}C + AC$) untuk menjamin bahwa saat variabel transisi berubah, term redundan mempertahankan logika 1 tanpa bergantung pada jalur inverter yang lambat."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi penyederhana Karnaugh Map (K-Map) 4-variabel yang mengidentifikasi seluruh prime implicant dan menghasilkan fungsi Boolean Sum-of-Products (SOP) minimal.
- **Petunjuk Perancangan Arsitektur**:
  - Representasikan minterm dalam format biner dan kelompokkan berdasarkan jumlah bit 1 (metode Quine-McCluskey).
  - Tentukan prime implicant esensial yang mencakup minterm unik.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi Paritas Ganjil (XOR 4-Input)*: K-Map papan catur murni; verifikasi tidak ada prime implicant yang dapat digabung (membutuhkan 8 term terpisah).
  - *Tautologi Penuh*: Minterm mencakup seluruh $0 \dots 15$; hasil penyederhanaan harus tepat bernilai konstanta $1$.
- **Rubrik Penilaian Mandiri**: 40% Algoritma Quine-McCluskey / K-Map Bitwise Presisi, 30% Identifikasi Prime Implicant Esensial Tepat, 30% Validasi Fungsi Tautologi & XOR Ekstrem.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan penganalisis Static Hazard otomatis pada rangkaian gerbang bertingkat (multi-level gate network) yang mendeteksi pasangan transisi input yang memicu static-0 hazard atau static-1 hazard, dan secara otomatis menambahkan term redundan penutup.
- **Petunjuk Perancangan Arsitektur**:
  - Evaluasi transisi adjacent input dengan jarak Hamming tepat 1.
  - Periksa apakah transisi tersebut melintasi perbatasan dua kelompok prime implicant terpisah pada K-Map tanpa penutup redundan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Fungsi $F = AB + \bar{B}C$*: Deteksi static-1 hazard saat $A=1, C=1$ dan $B$ beralih; sintesiskan term penutup otomatis $AC$.
  - *Rangkaian Bebas Hazard*: Uji fungsi $F = AB + \bar{B}C + AC$; verifikasi laporan output 100% bebas glitch.
- **Rubrik Penilaian Mandiri**: 40% Deteksi Transisi K-Map Jarak Hamming 1 Tepat, 30% Algoritma Sintesis Term Penutup Konsensus Redundan, 30% Verifikasi Bebas Glitch Rangkaian Terkoreksi.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator timing akurat tingkat gerbang (Gate-Level Timing Simulator) berbasis antrean kejadian (*event-driven simulation engine*) dalam Python untuk mengevaluasi dinamika perambatan delay min/max (transport delay & inertial delay) dan mendeteksi penolakan pulsa runt (*runt pulse filtering*) pada flip-flop sinkron.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan model penundaan inersial: pulsa input yang durasinya lebih pendek dari keterlambatan gerbang ($t_{pulse} < t_{pd}$) harus ditolak dan tidak merambat ke output.
  - Selesaikan penjadwalan transisi sinyal menggunakan antrean prioritas waktu (*time-ordered priority queue*).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penolakan Pulsa Inersial*: Berikan pulsa sempit $0.5\text{ ns}$ pada gerbang dengan $t_{pd} = 1.0\text{ ns}$; verifikasi output gerbang tetap tidak berubah (pulsa tertolak).
  - *Transport Delay Murni*: Kawat transmisi panjang merambatkan pulsa tanpa atenuasi durasi waktu.
- **Rubrik Penilaian Mandiri**: 40% Event-Driven Simulation Engine Prioritas Antrean Presisi, 30% Implementasi Model Inertial vs Transport Delay Tepat, 30% Deteksi Runt Pulse & Pelanggaran Sinyal Gate-Level."""
    },
    54: {
        "trace": r"""#### Tabel Penelusuran Perambatan Carry Ripple Carry Adder (RCA) 32-Bit Menghambat Clock Prosesor
| Tahap Bit Adder ($k$) | Masukan Operand ($A_k, B_k$) | Operasi Bitwise ($P_k = A \oplus B, G_k = A \cdot B$) | Carry-In Masuk ($C_k$) | Waktu Tiba Sinyal Carry ($t_{arrive}$) | Status Keterlambatan Jalur Kritis |
|---|---|---|---|---|---|
| Bit 0 (LSB) | $A_0 = 1, B_0 = 1$ | $P_0 = 0, G_0 = 1$ (Carry dibangkitkan) | $C_0 = 0$ | $t = 0.10\text{ ns}$ | $C_1 = 1$ siap dirambatkan |
| Bit 1 | $A_1 = 1, B_1 = 0$ | $P_1 = 1$ (Carry dirambatkan) | $C_1 = 1$ | $t = 0.22\text{ ns}$ ($+0.12\text{ ns}$ per Full Adder) | $C_2 = 1$ diteruskan |
| Bit 15 (Tengah) | $A_{15} = 1, B_{15} = 0$ | $P_{15} = 1$ | $C_{15} = 1$ | $t = 1.90\text{ ns}$ | Rantai carry merambat lambat |
| Bit 31 (MSB Terakhir) | $A_{31} = 1, B_{31} = 0$ | $P_{31} = 1$ | $C_{31} = 1$ | $t = 3.82\text{ ns}$ ($32 \times 0.12\text{ ns}$ akumulasi) | Carry baru tiba di gerbang MSB! |
| Clock Siklus CPU | Frekuensi CPU $= 500\text{ MHz}$ | Periode Jam $T_{clk} = 2.00\text{ ns}$ | Waktu perambatan $3.82\text{ ns} > 2.00\text{ ns}$! | Register ALU men-sample nilai acak sampah | Penjumlahan ALU korup! CPU hang crash |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Keterlambatan Perambatan Bawaan Ripple Carry Adder (RCA) Menghambat Frekuensi Jam CPU",
            "chronology": r"""- **Insiden Kegagalan Overclocking Prosesor Awal**: Pada era awal mikroprosesor 32-bit eksperimental, insinyur mencoba menaikkan frekuensi kerja jam CPU dari 100 MHz ke 400 MHz. Unit eksekusi integer mulai menghasilkan kesalahan perhitungan matematika acak pada instruksi penjumlahan (`ADD`), di mana angka-angka besar yang menghasilkan perambatan carry panjang menghasilkan nilai keluaran yang sepenuhnya salah.
- **Akar Masalah Rangkaian Logika Kombinasional & Kompleksitas Linier RCA**: Penjumlahan biner 32-bit yang disusun menggunakan kaskade berantai Full Adder standar (Ripple Carry Adder / RCA) memiliki ketergantungan sekuensial yang ketat: setiap bit $k$ tidak dapat menghitung hasil bit jumlah $S_k$ atau carry keluar $C_{k+1}$ sebelum carry dari bit sebelumnya $C_k$ selesai dihitung dan tiba secara fisik. Keterlambatan perambatan total berskala linier $\mathcal{O}(N)$. Untuk penjumlah 32-bit dengan penundaan gerbang $120\text{ ps}$ per stage, carry membutuhkan waktu hampir $4\text{ ns}$ untuk merambat dari LSB ke MSB. Ketika periode jam CPU dipersingkat menjadi $2\text{ ns}$ (frekuensi 500 MHz), pulsa jam berikutnya tiba saat carry baru merambat sampai bit ke-16. Register ALU men-sample data yang belum selesai dihitung (*setup time violation* masif), merusak seluruh register dan instruksi percabangan program.""",
            "snippet": r"""```verilog
// Arsitektur Carry Lookahead Adder (CLA) 4-Bit Hirarkis: Kompleksitas O(log N)
module carry_lookahead_adder_4bit (
    input  wire [3:0] A, B,
    input  wire       Cin,
    output wire [3:0] Sum,
    output wire       Cout,
    output wire       P_group, G_group
);
    // 1. Bitwise Generate (G) dan Propagate (P) - dihitung paralel serentak dalam 1 gate delay
    wire [3:0] G = A & B;
    wire [3:0] P = A ^ B;

    // 2. Lookahead Carry Generator Logic - dihitung langsung dalam 2 gate delay tanpa riak berantai:
    wire C1 = G[0] | (P[0] & Cin);
    wire C2 = G[1] | (P[1] & G[0]) | (P[1] & P[0] & Cin);
    wire C3 = G[2] | (P[2] & G[1]) | (P[2] & P[1] & G[0]) | (P[2] & P[1] & P[0] & Cin);
    assign Cout = G[3] | (P[3] & G[2]) | (P[3] & P[2] & G[1]) | (P[3] & P[2] & P[1] & G[0]) | (P[3] & P[2] & P[1] & P[0] & Cin);

    // 3. Sum bits dihitung paralel: Sum = P ^ Carry
    assign Sum[0] = P[0] ^ Cin;
    assign Sum[1] = P[1] ^ C1;
    assign Sum[2] = P[2] ^ C2;
    assign Sum[3] = P[3] ^ C3;

    // Sinyal Propagate dan Generate untuk grup tingkat berikutnya
    assign P_group = &P;
    assign G_group = Cout; // Carry terhitung instan dalam O(1) waktu!
endmodule
```""",
            "analysis": r"""- **Arsitektur Penjumlah Kecepatan Tinggi Modern**: Desain CPU modern sepenuhnya meninggalkan RCA dan mengadopsi arsitektur penjumlah logaritmik $\mathcal{O}(\log N)$ seperti Kogge-Stone Adder, Brent-Kung Adder, atau Han-Carlson Parallel Prefix Adder. Algoritma ini menggunakan struktur pohon prefiks paralel (*prefix tree*) untuk menghitung seluruh carry secara serentak dalam $\log_2(N)$ tahapan gerbang, memungkinkan operasi penambahan 64-bit diselesaikan dalam waktu kurang dari $200\text{ ps}$ pada prosesor multi-gigahertz."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul struktural Verilog untuk Full Adder 1-bit dan rangkai menjadi Ripple Carry Adder (RCA) 8-bit, lalu buat testbench untuk memverifikasi penjumlahan seluruh vektor kasus uji.
- **Petunjuk Perancangan Arsitektur**:
  - Full Adder: $S = A \oplus B \oplus C_{in}$, $C_{out} = (A \cdot B) + (C_{in} \cdot (A \oplus B))$.
  - Hubungkan $C_{out}$ stage $k$ ke $C_{in}$ stage $k+1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Kasus Perambatan Carry Terpanjang*: $A = 0\text{xFF}, B = 0\text{x01}$; verifikasi hasil $Sum = 0\text{x00}$ dan $C_{out} = 1$.
  - *Penjumlahan Nol*: $A = 0\text{x00}, B = 0\text{x00}, C_{in} = 0$; $Sum = 0, C_{out} = 0$.
- **Rubrik Penilaian Mandiri**: 40% Modul Full Adder & Instansiasi Berantai Verilog Tepat, 30% Testbench Menyeluruh untuk Kasus Worst-Case Carry, 30% Verifikasi Flag Overflow & Carry Out.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan modul Carry Lookahead Adder (CLA) 16-bit hirarkis (terdiri dari 4 blok CLA 4-bit dan 1 unit Lookahead Carry Generator tingkat atas), bandingkan jumlah gerbang dan delay maksimum terhadap RCA 16-bit.
- **Petunjuk Perancangan Arsitektur**:
  - Hitung sinyal Propagate grup ($P_G$) dan Generate grup ($G_G$) pada setiap blok 4-bit.
  - Unit Lookahead tingkat atas menghitung carry masuk antar-blok $C_4, C_8, C_{12}, C_{16}$ dalam 2 keterlambatan gerbang.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pohon Perambatan Carry*: Verifikasi keterlambatan perambatan konstan bebas dari panjang rantai carry.
  - *Vektor Uji Komparatif*: Uji $A = 0\text{xAAAA}, B = 0\text{x5555}, C_{in} = 1$; hasil harus $Sum = 0\text{x0000}, C_{out} = 1$.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur CLA Hirarkis 2-Tingkat Presisi, 30% Evaluasi Perbandingan Delay Gerbang CLA vs RCA, 30% Verifikasi Integritas Hasil Penjumlahan 16-Bit.

### Tingkat 3: Mahir
- **Tugas**: Rancang sintesis generator otomatis Kogge-Stone Parallel-Prefix Adder 64-bit dalam Python/Verilog yang mengonstruksikan graf perambatan prefiks pohon asiklik, meminimalkan fan-out beban logika dan memverifikasi fungsionalitas formal ekuivalensi matematis menggunakan Z3 Theorem Prover.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan operator prefiks biner asosiatif $\circ$: $(g, p) \circ (g', p') = (g + p \cdot g', p \cdot p')$.
  - Bangun $\log_2(64) = 6$ tahapan prefix tree dengan fan-out maksimum terikat $\le 2$ pada setiap node.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Verifikasi Formal Z3*: Buktikan secara simbolik bahwa untuk setiap kemungkinan pasangan input 64-bit $(A, B)$, output adder Kogge-Stone identik dengan $A + B + C_{in}$.
  - *Evaluasi Keterlambatan Jalur Kritis*: Total keterlambatan gerbang tidak boleh melampaui $1 + 2 \times \log_2(N) = 13$ gerbang logika.
- **Rubrik Penilaian Mandiri**: 40% Generator Kogge-Stone Prefix Network Bitwise Presisi, 30% Pembuktian Formal Matematika dengan Z3 Solver, 30% Optimasi Fan-Out & Keterlambatan Gerbang Logaritmik."""
    },
    55: {
        "trace": r"""#### Tabel Penelusuran Konversi 64-Bit Float ke 16-Bit Integer & Ledakan Roket Ariane 5 (1996)
| Detik Pasca Peluncuran ($t$) | Besaran Fisik (Kecepatan Horizontal) | Nilai Floating Point 64-Bit IEEE 754 | Upaya Konversi ke `int16_t` Bertanda | Status Exception / Register Perangkat Keras | Dampak Tindakan Komputer Navigasi |
|---|---|---|---|---|---|
| $t = 0.0\text{ s}$ | $0.0\text{ m/s}$ (Roket lepas landas) | `0x0000_0000_0000_0000` ($0.0$) | Konversi sukses: `0x0000` ($0$) | Operasi normal | Sistem kendali sikap roket stabil |
| $t = 30.0\text{ s}$ | $150.0\text{ m/s}$ | `0x4062_C000_0000_0000` ($150.0$) | Konversi sukses: `0x0096` ($150$) | Operasi normal | Trajektori roket sempurna |
| $t = 36.7\text{ s}$ | $32.760.0\text{ m/s}$ (Mendekati batas 16-bit) | `0x40DFF80000000000` ($32760.0$) | Konversi sukses: `0x7FF8` ($32760$) | Rentang nilai signed 16-bit tersisa 7 unit | Roket berakselerasi sangat cepat |
| $t = 36.8\text{ s}$ (Overheat Batas) | $32.768.5\text{ m/s}$ ($> 32.767$!) | `0x40E0_0010_0000_0000` | Meluap melampaui kapasitas signed 16-bit! | Hardware Operand Error Trap terpicu! | Exception tidak ditangani blok try-catch |
| $t = 36.9\text{ s}$ (Crash Komputer) | Komputer primer mencetak crash dump | Dump diagnostik dikirim ke bus avionik | Aktuator nozzle mengira dump adalah data sudut kemudi!| Nozzle roket dibelokkan ke batas ekstrem $90^\circ$! | Beban aerodinamis mematahkan roket; meledak! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Ledakan Roket Ariane 5 Penerbangan 501 (1996) Akibat Konversi 64-bit Float ke 16-bit Integer",
            "chronology": r"""- **Kronologi Bencana Kedirgantaraan**: Pada 4 Juni 1996, roket luar angkasa Eropa Ariane 5 meledak berkeping-keping hanya 37 detik setelah peluncuran perdana dari Kourou, Guyana Prancis, menghancurkan muatan satelit ilmiah bernilai lebih dari $370 juta.
- **Akar Masalah Representasi Bilangan & Truncation Overflow**: Perangkat lunak sistem referensi inersial (SRI) menggunakan kembali modul kode dari roket pendahulunya, Ariane 4. Modul ini menghitung nilai variabel *Horizontal Bias* ($BH$) yang merepresentasikan kecepatan horizontal roket dalam format IEEE 754 floating-point 64-bit, yang kemudian dikonversikan ke signed integer 16-bit (rentang nilai $-32.768$ hingga $+32.767$). Pada roket Ariane 4 yang lebih lambat, nilai $BH$ secara fisik terbukti tidak akan pernah melampaui 32.767, sehingga pengembang mematikan proteksi exception handler untuk menghemat siklus CPU. Namun, roket Ariane 5 memiliki mesin berdaya dorong jauh lebih dahsyat dengan trajektori akselerasi lebih curam. Tiga puluh enam detik setelah peluncuran, nilai kecepatan horizontal melampaui 32.767. Konversi memicu *hardware arithmetic overflow exception*. Karena ketiadaan blok penanganan exception di kode Ada, kedua komputer navigasi (primer dan cadangan identik) mengalami crash dan berhenti beroperasi serentak, memuntahkan pesan diagnostik kesalahan memori ke saluran data kendali. Komputer kemudi utama salah menafsirkan bit-bit pesan crash ini sebagai perintah defleksi sirip kemudi, membelokkan nozzle mesin roket hingga sudut maksimum 90 derajat hingga roket patah akibat gaya geser aerodinamis.""",
            "snippet": r"""```c
// Rekonstruksi C/Ada Cacat Overflow Konversi Tipe Data Ariane 5
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef struct {
    int16_t horizontal_bias_raw;
    bool hardware_trap_raised;
} NavigationData;

NavigationData unsafe_convert_horizontal_bias(double horizontal_velocity_m_s) {
    NavigationData nav;
    // Cacat Ariane 5: Tidak ada pemeriksaan batas (clamping) sebelum casting!
    // Pada arsitektur Ada/M68020, casting float > 32767 ke 16-bit memicu trap CPU
    if (horizontal_velocity_m_s > 32767.0 || horizontal_velocity_m_s < -32768.0) {
        nav.hardware_trap_raised = true; // CPU EXCEPTION: Arithmetic Overflow!
        nav.horizontal_bias_raw = 0;     // Komputer crash mati seketika
    } else {
        nav.hardware_trap_raised = false;
        nav.horizontal_bias_raw = (int16_t)horizontal_velocity_m_s;
    }
    return nav;
}

// Mitigasi modern: Saturating Arithmetic (Clamping ke rentang maksimum aman)
int16_t safe_saturating_convert(double val) {
    if (val > 32767.0) return 32767;
    if (val < -32768.0) return -32768;
    return (int16_t)val;
}
```""",
            "analysis": r"""- **Pelajaran Rekayasa Perangkat Lunak Kritis**: Insiden Ariane 5 adalah contoh abadi bahaya penggunaan kembali perangkat lunak (*software reuse*) tanpa memvalidasi ulang asumsi domain fisik pada sistem baru. Komisi Penyelidikan mengamanatkan bahwa seluruh konversi tipe data yang berpotensi meluap wajib dilindungi penanganan eksepsi eksplisit, dan kode diagnostik tidak boleh dieksekusi di saluran bus aktuator aktif."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi encoder dan decoder representasi floating-point standar IEEE 754 presisi tunggal (32-bit: 1-bit sign, 8-bit exponent dengan bias 127, 23-bit fraction/mantissa) dalam Python murni tanpa pustaka eksternal.
- **Petunjuk Perancangan Arsitektur**:
  - Tangani bilangan normal: $(-1)^s \times 2^{e - 127} \times (1 + f)$.
  - Tangani bilangan subnormal: $(-1)^s \times 2^{-126} \times (0 + f)$.
  - Tangani representasi khusus: $+0.0, -0.0, +\infty, -\infty,$ dan NaN.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Bilangan Normal*: Nilai $-0.15625$; verifikasi representasi heksadesimal tepat `0xBE200000`.
  - *Subnormal Terkecil*: Nilai biner `0x00000001`; verifikasi konversi ke desimal $\approx 1.401298 \times 10^{-45}$.
- **Rubrik Penilaian Mandiri**: 40% Dekomposisi Bitwise IEEE 754 Presisi, 30% Penanganan Benar Subnormal Denormalized Numbers, 30% Penanganan Khusus Nilai Inf dan NaN.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan pustaka aritmatika titik tetap (*Fixed-Point Arithmetic Library*) format Q-format generik (misal Q15.16 atau Q8.8) dengan dukungan mode pembulatan (*rounding modes: truncation, convergent round-to-even*) dan mode luapan (*overflow modes: wrap-around vs saturating arithmetic*).
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan saturasi: jika hasil perkalian atau penambahan melampaui batas batas $MAX\_VAL$, jepit nilai tepat di $MAX\_VAL$ alih-alih membiarkan wrap-around.
  - Untuk perkalian $Q_{m.n} \times Q_{m.n}$, gunakan accumulator 64-bit perantara sebelum pembulatan dan pemotongan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Saturating Overflow*: Penambahan dua nilai positif maksimum; verifikasi hasil terkunci di $0\text{x7FFF\_FFFF}$ tanpa membalik tanda menjadi negatif.
  - *Presisi Pembulatan Round-to-Even*: Evaluasi pembulatan nilai tepat di tengah ($0.5\text{ LSB}$); verifikasi pembulatan ke digit genap terdekat.
- **Rubrik Penilaian Mandiri**: 40% Operasi Bitwise Fixed-Point Q-Format Tepat, 30% Implementasi Saturating Arithmetic Bebas Wrap-Around, 30% Algoritma Pembulatan Convergent Round-to-Even.

### Tingkat 3: Mahir
- **Tugas**: Rancang penganalisis propagasi galat pembulatan (*Floating-Point Round-Off Error Propagation Analyzer*) menggunakan aritmatika interval (*Interval Arithmetic*) untuk memverifikasi batas galat numerik akumulatif pada algoritma iteratif Kalman Filter atau matriks inversi, serta mendeteksi potensi fenomena pembatalan katastropik (*catastrophic cancellation*).
- **Petunjuk Perancangan Arsitektur**:
  - Definisikan operasi interval: $[x_1, x_2] + [y_1, y_2] = [x_1 + y_1, x_2 + y_2]$ dan perkalian interval dengan pembulatan ke luar terarah (*directed outward rounding*).
  - Identifikasi operasi pengurangan dua bilangan floating point yang hampir identik ($x \approx y$) di mana jumlah digit signifikan valid hilang drastis.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Pembatalan Katastropik*: Hitung fungsi $f(x) = \sqrt{x+1} - \sqrt{x}$ untuk $x = 10^8$; buktikan kehilangan presisi pada evaluasi langsung dan verifikasi pemulihan presisi via formulasi aljabar konjugat $\frac{1}{\sqrt{x+1} + \sqrt{x}}$.
  - *Batas Interval Tervalidasi*: Buktikan bahwa nilai matematis sejati selalu berada di dalam rentang interval terhitung $[\underline{x}, \bar{x}]$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Interval Arithmetic Operasi Dasar Presisi, 30% Deteksi Otomatis Kondisi Catastrophic Cancellation, 30% Verifikasi Batas Galat Penjaminan Ketat."""
    },
    56: {
        "trace": r"""#### Tabel Penelusuran Pelanggaran Waktu Setup/Hold & Fenomena Metastabilitas pada Clock Domain Crossing (CDC)
| Domain Jam Asal (Domain A) | Sinyal Data Berubah ($Data_A$) | Domain Jam Tujuan (Domain B, $Clk_B$) | Selisih Waktu Transisi Data vs Tepi Jam | Status Tegangan Output Flip-Flop B1 ($Q_1$) | Efek pada Pointer FIFO Antrean |
|---|---|---|---|---|---|
| Jam $100\text{ MHz}$ | Data beralih $0 \to 1$ | Jam Asinkron $133\text{ MHz}$ | Data berubah tepat di jendela $t_{setup}/t_{hold}$ | Melanggar batas waktu setup internal ($< 50\text{ ps}$)| Transistor CMOS masukan seimbang semu |
| Siklus 1 $Clk_B$ | Data stabil 1 | Tepi naik jam $Clk_B$ tiba | Terjadi perebutan muatan di node bistabil | Tegangan melayang di ambang batas $V_{DD}/2 = 1.65\text{ V}$| METASTABILITAS! Status logika bukan 0 dan bukan 1! |
| Periode Resolusi | Osilasi dering internal | Waktu resolusi $\tau_{met}$ berjalan | $Q_1$ lambat meluruh menuju level valid | Tegangan berfluktuasi liar selama $1.8\text{ ns}$ | Gerbang logika penerima melihat nilai berbeda-beda! |
| Tanpa Penyelaras Ganda | Sinyal metastabil dibaca logika | Decoder alamat membaca nilai abu-abu | Bit biner terinterpretasi 0 di satu blok, 1 di blok lain | Pointer FIFO korup melompat acak | Pointer FIFO melonjak; buffer over-read |
| Dengan 2-Flip-Flop Sync | $Q_1$ metastabil terkurung | Tepi jam ke-2 tiba pada flip-flop B2 | Tegangan $Q_1$ sudah meluruh stabil ke 1 | Flip-flop B2 men-sample data 1 valid bersih | MTBF melonjak dari 3 detik ke $> 100.000$ tahun! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Metastabilitas pada Clock Domain Crossing (CDC) Asinkron Tanpa 2-Stage Synchronizer",
            "chronology": r"""- **Insiden Kegagalan Switch Jaringan Telekomunikasi**: Pada switch paket jaringan berkecepatan 10 Gbps, paket data secara misterius mengalami korupsi data acak rata-rata sekali setiap dua hari di bawah beban lalu lintas tinggi. Analisis log sistem menunjukkan buffer FIFO transmisi mengalami korupsi pointer tulis-baca, menyebabkan paket tertimpa dan memicu reset port darurat.
- **Akar Masalah Rangkaian Logika Sekuensial & Metastabilitas Silikon**: Sistem memiliki dua domain clock independen yang asinkron: domain clock pemrosesan paket 156,25 MHz dan domain clock bus memori 200 MHz. Seorang pengembang memindahkan sinyal bendera kendali (*flag control signal*) secara langsung melintasi batas domain clock tanpa menggunakan rangkaian penyelaras (*synchronizer*). Ketika sinyal data dari domain pertama beralih status tepat di dalam jendela waktu setup/hold dari flip-flop penerima di domain kedua, gerbang bistabil internal flip-flop tidak dapat memutuskan apakah input bernilai 0 atau 1. Tegangan keluaran melayang di titik ekuilibrium tidak stabil di sekitar ambang batas logika $V_{DD}/2$ selama rentang waktu tak terduga (*metastable state*). Sinyal metastabil ini merambat ke beberapa gerbang logika penerima; karena perbedaan ambang batas tegangan gerbang silikon, sebagian gerbang menginterpretasikannya sebagai logika 1 sementara gerbang lain menginterpretasikannya sebagai logika 0, memicu korupsi pointer memori FIFO.""",
            "snippet": r"""```verilog
// Rangkaian Clock Domain Crossing (CDC) Aman: 2-Flip-Flop Synchronizer
module cdc_2ff_synchronizer #(
    parameter WIDTH = 1
)(
    input  wire             clk_dst,     // Domain clock penerima
    input  wire             rst_n,
    input  wire [WIDTH-1:0] async_in,    // Sinyal dari domain clock asal
    output reg  [WIDTH-1:0] sync_out     // Sinyal aman bebas metastabilitas
);
    // Tingkat 1: Mengisolasi kondisi metastabil
    reg [WIDTH-1:0] meta_reg;

    always @(posedge clk_dst or negedge rst_n) begin
        if (!rst_n) begin
            meta_reg <= {WIDTH{1'b0}};
            sync_out <= {WIDTH{1'b0}};
        end else begin
            meta_reg <= async_in; // Jika meta_reg metastabil, tegangan meluruh selama 1 periode clock
            sync_out <= meta_reg; // sync_out men-sample data bersih teregulasi
        end
    end
    // Catatan: Hanya aman untuk sinyal kendali level 1-bit atau sinyal ber-kode Gray!
endmodule
```""",
            "analysis": r"""- **Formula MTBF Metastabilitas & Protokol CDC Multi-Bit**: Mean Time Between Failures dari sebuah rangkaian penangkap sinyal asinkron diformulasikan sebagai: $MTBF = \frac{e^{t_{resolve} / \tau}}{T_0 \cdot f_{clk} \cdot f_{data}}$. Menyisipkan flip-flop kedua menyediakan waktu resolusi tambahan ($t_{resolve} = T_{clk} - t_{setup}$), menaikkan nilai MTBF secara eksponensial dari skala detik menjadi jutaan tahun. Selain itu, untuk bus multi-bit, penyelaras 2-FF tidak boleh digunakan langsung; arsitektur wajib menggunakan pengkodean biner *Gray Code* (di mana hanya 1 bit yang berubah per transisi) atau arsitektur Asynchronous FIFO lengkap dengan handshaking ganda."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul Verilog D-Flip-Flop dengan reset asinkron active-low dan enable clock, verifikasi fungsi penyimpanan data dan kekebalan terhadap perubahan data saat clock diam.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan sintaks standar: `always @(posedge clk or negedge rst_n)`.
  - Jika `!rst_n`, $Q \leftarrow 0$; jika `en`, $Q \leftarrow D$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Asynchronous Reset*: Berikan pulsa reset $rst\_n = 0$ di antara tepi clock; buktikan output $Q$ langsung kembali ke 0 seketika tanpa menunggu tepi clock.
  - *Clock Enable Disabled*: Set $en = 0$; buktikan $Q$ mempertahankan nilai lama meskipun $D$ berubah bebas pada setiap tepi clock.
- **Rubrik Penilaian Mandiri**: 40% Sintaks Verilog Sequential D-FF Standar Presisi, 30% Penanganan Reset Asinkron Prioritas Tertinggi, 30% Verifikasi Logika Clock Enable.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan kalkulator Mean Time Between Failures (MTBF) metastabilitas untuk antarmuka Clock Domain Crossing (CDC) berdasarkan parameter teknologi proses semikonduktor ($\tau, T_0$), frekuensi clock penerima ($f_{clk}$), frekuensi peralihan data ($f_{data}$), dan waktu kelonggaran penyelesaian ($\Delta t$).
- **Petunjuk Perancangan Arsitektur**:
  - Formulasikan persamaan MTBF: $MTBF = \frac{\exp(\Delta t / \tau)}{T_0 \cdot f_{clk} \cdot f_{data}}$.
  - Hitung perbedaan MTBF antara penyelaras 1-tahap ($\Delta t_1 = T_{clk} - t_{setup}$) vs penyelaras 2-tahap ($\Delta t_2 = 2 T_{clk} - t_{setup}$).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penyelaras 1-Stage*: $f_{clk} = 100\text{ MHz}, f_{data} = 10\text{ MHz}, \tau = 50\text{ ps}, T_0 = 100\text{ ps}$; buktikan MTBF hanya beberapa jam/hari.
  - *Penyelaras 2-Stage*: Menambahkan tahap ke-2 melonjakkan MTBF melampaui $10^9\text{ tahun}$.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matematika MTBF Metastabilitas Tepat, 30% Perhitungan Eksponensial Multi-Stage Synchronizer, 30% Analisis Sensitivitas Terhadap Frekuensi Clock.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul Asynchronous FIFO (Dual-Clock FIFO) lengkap dalam Verilog synthesizable yang menjembatani transfer data antar-dua domain clock independen ($clk_{wr}$ dan $clk_{rd}$), gunakan konversi biner-ke-Gray untuk pointer tulis dan baca, sinkronisasikan pointer Gray menggunakan 2-stage synchronizer, serta turunkan logika pembangkit bendera `full` dan `empty` yang terbukti bebas kondisi balapan (*race condition*).
- **Petunjuk Perancangan Arsitektur**:
  - Pointer biner ke Gray: `gray = bin ^ (bin >> 1)`.
  - Kondisi Empty: `rd_ptr_gray == wr_ptr_gray_synchronized`.
  - Kondisi Full: dua bit tertinggi berbeda nilai, seluruh bit sisanya identik: `wr_ptr_gray == {~rd_ptr_gray[ADDR:ADDR-1], rd_ptr_gray[ADDR-2:0]}`.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transmisi Kontinu Kecepatan Penuh*: Uji penulisan terus-menerus hingga kondisi Full; verifikasi tidak ada data yang tertimpa (*zero overwrite*).
  - *Pengosongan Penuh*: Baca hingga bendera Empty aktif; verifikasi tidak ada pembacaan data usang (*zero underflow*).
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Dual-Clock Asynchronous FIFO Gray-Code Presisi, 30% Logika Generasi Bendera Full/Empty Bebas Glitch, 30% Verifikasi Formal Ketiadaan Korupsi Memori."""
    },
    57: {
        "trace": r"""#### Tabel Penelusuran Kunci State Tak Terjangkau (Unreachable State Lockup) pada FSM One-Hot Lampu Lalu Lintas
| Siklus Jam ($Clk$) | Status State Legal FSM | Vektor Enkode One-Hot ($S_3 S_2 S_1 S_0$) | Radiasi Partikel Kosmik (Single Event Upset) | Vektor State Pascacorruption | Reaksi Logika Transisi State FSM |
|---|---|---|---|---|---|
| Siklus 0 | STATE_RED | `0001` (Bobot Hamming = 1) | Tidak ada | `0001` (Legal) | Transisi normal ke STATE_GREEN |
| Siklus 1 | STATE_GREEN | `0010` (Bobot Hamming = 1) | Tidak ada | `0010` (Legal) | Transisi normal ke STATE_YELLOW |
| Siklus 2 | STATE_YELLOW | `0100` (Bobot Hamming = 1) | Neutron kosmik membalik bit 3 ($0 \to 1$)| `1100` (ILLEGAL! Dua bit 1 bersamaan!)| State `1100` tidak didefinisikan dalam diagram! |
| Siklus 3 (Tanpa Default) | State tak dikenal `1100` | Logika `case` tidak menemukan kecocokan| Tidak ada cabang `default` pemulihan | State mempertahankan nilai `1100` | FSM TERKUNCI PERMANEN! Lampu mati membeku |
| Siklus 4 (Sistem Macet) | Terkunci selamanya | `1100` | Lampu lalu lintas tidak berganti siklus | Tetap macet di `1100` | Tabrakan di persimpangan jalan raya |
| Dengan Safe Recovery | State tak dikenal `1100` | Cabang `default` mendeteksi anomali | Eksekusi reset darurat otomatis | Mengatur ulang ke `0001` (RED aman) | FSM pulih mandiri dalam 1 siklus jam! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Pengontrol Lampu Lalu Lintas Terkunci Permanen pada State Tak Terjangkau (Unreachable State Lockup)",
            "chronology": r"""- **Insiden Kegagalan Pengendali Persimpangan Kota**: Di persimpangan jalan protokol metropolitan yang sibuk, unit pengontrol lampu lalu lintas digital mendadak membeku di tengah jam sibuk. Seluruh lampu indikator mati dan sistem berhenti merespons sensor kendaraan. Polisi lalu lintas terpaksa turun tangan mengatur manual di tengah kemacetan total.
- **Akar Masalah Mesin Keadaan Hingga (FSM) & Enkode One-Hot Tanpa Pemulihan**: Pengontrol dirancang menggunakan FSM dengan skema pengkodean One-Hot (4 state direpresentasikan oleh 4 bit register: `0001`, `0010`, `0100`, `1000`). Pada pengkodean 4-bit, terdapat $2^4 = 16$ kombinasi nilai biner, namun hanya 4 kombinasi yang merupakan status legal (jarak bobot Hamming = 1), sedangkan 12 kombinasi lainnya adalah *unreachable illegal states*. Akibat lonjakan derau listrik atau partikel radiasi kosmik (*Single Event Upset* / SEU), sebuah bit register mengalami *bitflip* dari `0100` menjadi `1100`. Di dalam kode HDL, perancang menulis struktur `case (state)` tanpa menambahkan klausul `default: state <= STATE_RESET;` karena menganggap secara matematis state ilegal tidak akan pernah tercapai. Kompilator sintesis mengoptimalkan logika transisi dengan mengabaikan 12 kombinasi ilegal tersebut. Begitu FSM terperosok ke dalam state `1100`, tidak ada persamaan transisi yang memindahkan register ke mana-mana, mengunci FSM dalam deadlock abadi yang hanya bisa dipulihkan dengan memutus daya secara fisik.""",
            "snippet": r"""```verilog
// Arsitektur Finite State Machine Aman (Safe FSM with Auto-Recovery)
module traffic_light_safe_fsm (
    input  wire clk,
    input  wire rst_n,
    input  wire timer_done,
    output reg [1:0] light_code // 00: Red, 01: Green, 10: Yellow
);
    // Definisi State One-Hot
    localparam [3:0] ST_RED    = 4'b0001,
                     ST_GREEN  = 4'b0010,
                     ST_YELLOW = 4'b0100,
                     ST_ALLRED = 4'b1000;

    (* syn_encoding = "safe, one-hot" *) // Atribut instruksi sintesis safe FSM
    reg [3:0] current_state, next_state;

    // Logika Transisi Kombinasional
    always @(*) begin
        case (current_state)
            ST_RED:    next_state = timer_done ? ST_GREEN  : ST_RED;
            ST_GREEN:  next_state = timer_done ? ST_YELLOW : ST_GREEN;
            ST_YELLOW: next_state = timer_done ? ST_ALLRED : ST_YELLOW;
            ST_ALLRED: next_state = timer_done ? ST_RED    : ST_ALLRED;
            
            // KLAUSUL WAJIB PEMULIHAN DARI STATE ILEGAL:
            default:   next_state = ST_RED; // Pemulihan otomatis ke state aman!
        endcase
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) current_state <= ST_RED;
        else        current_state <= next_state;
    end
endmodule
```""",
            "analysis": r"""- **Standar Desain FSM Kritis (IEC 61508 / ISO 26262)**: Pada perancangan sistem keselamatan kritis (otomotif, medis, kedirgantaraan), penulisan FSM mewajibkan dua aturan: 1) Klausul `default` wajib ada untuk menangani seluruh status sisa $2^N - M$; 2) Menambahkan logika pengecekan paritas atau deteksi bobot Hamming untuk mendeteksi *illegal state* dan secara proaktif membangkitkan sinyal peringatan kesalahan perangkat keras (*fault alarm*)."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun Finite State Machine tipe Moore dalam Verilog untuk mendeteksi urutan biner 4-bit spesifik (`1011`) pada aliran bit masukan serial satu-bit (Sequence Detector).
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan 5 status: `S_RESET`, `S_1`, `S_10`, `S_101`, `S_MATCH`.
  - Tangani kasus urutan bertindih (*overlapping sequence*, misal masukan `1011011` menghasilkan dua pulsa deteksi).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Aliran Masukan Overlapping*: String `1011011011`; verifikasi bahwa sinyal deteksi $Y$ aktif tepat 3 kali.
  - *Urutan Palsu*: String `10101010`; sinyal deteksi $Y$ harus tetap bernilai 0 di seluruh siklus.
- **Rubrik Penilaian Mandiri**: 40% Diagram State & Logika Transisi Moore Tepat, 30% Penanganan Overlapping Sequence Benar, 30% Testbench Komprehensif dengan Verifikasi Otomatis.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan mesin keadaan Mealy vs Moore untuk pengontrol antarmuka bus Serial Peripheral Interface (SPI) Slave Mode 0, bandingkan jumlah flip-flop yang dibutuhkan dan latensi keluaran sinyal kontrol.
- **Petunjuk Perancangan Arsitektur**:
  - Moore: Keluaran hanya bergantung pada state saat ini (keluaran terdaftar bersih, latensi 1 siklus).
  - Mealy: Keluaran bergantung pada state saat ini dan masukan saat ini (keluaran asinkron instan, rentan terhadap glitch masukan).
- **Test Vector & Kasus Uji Ekstrem**:
  - *Transmisi Byte 8-Bit*: Terapkan 8 siklus clock SCK; buktikan kedua mesin menggeser dan mengunci data secara identik.
  - *Glitch Masukan Mealy*: Injeksi derau transien pada pin masukan Mealy; buktikan munculnya glitch palsu pada sinyal keluaran Mealy yang tidak terjadi pada Moore.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Perbandingan Mealy vs Moore Presisi, 30% Analisis Latensi & Kerentanan Glitch Mealy, 30% Verifikasi Kepatuhan Protokol SPI Mode 0.

### Tingkat 3: Mahir
- **Tugas**: Rancang simulator FSM fault-injection otomatis dalam Python/Verilog yang menguji ketahanan FSM terhadap radiasi Single Event Upset (SEU) dengan menginjeksi bitflip acak pada setiap register state, mengklasifikasikan respons FSM (Pemulihan Mandiri Aman, Transisi Salah, atau Deadlock Tak Terjangkau), dan mengoptimalkan pengkodean state menggunakan Hamming Distance $\ge 3$ (SECDED Error Correcting Code).
- **Petunjuk Perancangan Arsitektur**:
  - Enkode state menggunakan kode linear Hamming $(7, 4)$ yang mampu mengoreksi 1 bitflip otomatis dan mendeteksi 2 bitflip.
  - Jika terjadi 1 bitflip, logika sindrom mengoreksi state kembali ke legal dalam siklus yang sama tanpa mengganggu operasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Injeksi 1 Bitflip Acak*: FSM mengoreksi bitflip secara transparan; transisi state berikutnya tetap $100\%$ akurat.
  - *Injeksi 2 Bitflip*: FSM mendeteksi kesalahan ganda tak terpulihkan dan melompat ke state fail-safe darurat.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur FSM Hamming SECDED Tepat, 30% Engine Injeksi SEU Acak Komprehensif, 30% Pembuktian Fungsionalitas Self-Healing Otomatis."""
    },
    58: {
        "trace": r"""#### Tabel Penelusuran Inferensi Kait Transparan Tak Disengaja (Inadvertent Latch Inference) pada RTL
| Sinyal Masukan ($Sel$) | Kondisi Pernyataan `if-else` | Penugasan Sinyal Output ($Y$) | Keputusan Kompilator Sintesis RTL | Struktur Perangkat Keras Fisik yang Disintesis | Dampak Integritas Timing & Pengujian |
|---|---|---|---|---|---|
| $Sel = 0$ | Cabang `if (Sel == 0)` terpenuhi | $Y = Data\_A$ | Penugasan eksplisit | Gerbang multiplexer standar | Jalur kombinasi normal |
| $Sel = 1$ | Cabang `else if (Sel == 1)` terpenuhi | $Y = Data\_B$ | Penugasan eksplisit | Gerbang multiplexer standar | Jalur kombinasi normal |
| $Sel = 2$ | Tidak ada cabang yang cocok! | Nilai $Y$ tidak dispesifikasikan! | Kompilator berasumsi: "Nilai $Y$ harus dipertahankan!" | Disintesis menjadi Transparent D-Latch Fisik! | Komponen memori asinkron tak diinginkan tercipta! |
| $Sel = 3$ | Masukan terlarang | Nilai $Y$ tidak berubah | Latch menahan tegangan pada gerbang | Latch transparan fisik aktif saat Enable High | Jalur rentan terhadap glitch dan dering timing |
| Analisis Timing ASIC | Tool STA mengevaluasi jalur | Latch memiliki penundaan time-borrowing | Penutupan timing ASIC gagal | Boros area silikon & daya statis tinggi | Testability fault coverage ATPG ambruk |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Terbentuknya Kait Transparan Tak Disengaja (Inadvertent Latch Inference) pada Blok RTL",
            "chronology": r"""- **Insiden Kegagalan Timing Tape-Out FPGA/ASIC**: Pada desain chip pengendali memori berkecepatan tinggi, perangkat lunak sintesis logika melaporkan puluhan peringatan (*warnings*) yang diabaikan oleh pengembang junior: `Latch inferred for signal 'cmd_decode'`. Ketika desain dimuat ke dalam chip silikon fisik, chip mengalami kegagalan fungsi intermittent acak yang sangat peka terhadap perubahan suhu ruang.
- **Akar Masalah Hardware Description Language (HDL) & Logika Inkomplit**: Dalam bahasa Verilog/VHDL, blok kombinasi `always @(*)` dimaksudkan untuk menyintesis rangkaian kombinasional murni (gerbang AND/OR/MUX) tanpa elemen memori. Namun, sesuai semantik standar bahasa HDL, jika sebuah variabel tidak diberikan nilai penugasan pada setiap kemungkinan percabangan jalur eksekusi (`if-else` tanpa `else`, atau pernyataan `case` tanpa seluruh kemungkinan nilai input terpetakan), kompilator sintesis perangkat lunak terpaksa mengasumsikan bahwa rangkaian harus mempertahankan nilai variabel sebelumnya (*hold previous value*). Satu-satunya cara perangkat keras silikon dapat menahan nilai tanpa adanya sinyal clock sinkron adalah dengan menyintesis gerbang fisik kait transparan (*transparent D-latch*). Kait transparan ini bersifat peka level (*level-sensitive*), meloloskan derau glitch masukan secara langsung saat enable aktif, memicu loop balapan timing (*timing race conditions*), dan menggagalkan analisis timing statis (STA) serta pengujian otomatis manufaktur (ATPG scan testing).""",
            "snippet": r"""```verilog
// Contoh Buruk vs Contoh Bersih Penulisan Kombinasional RTL
module decoder_latch_bad (
    input  wire [1:0] sel,
    input  wire       data_in,
    output reg        out_bad,
    output reg        out_clean
);
    // POLA CACAT: Tidak ada cabang penutup 'else' atau default
    // Kompilator menyintesis Transparent Latch fisik untuk out_bad!
    always @(*) begin
        if (sel == 2'b00)
            out_bad = data_in;
        else if (sel == 2'b01)
            out_bad = ~data_in;
        // Jika sel == 2'b10 atau 2'b11, out_bad mempertahankan nilai lama -> LATCH INFERRED!
    end

    // POLA BERSIH: Seluruh cabang terpetakan, atau gunakan inisialisasi default awal
    always @(*) begin
        out_clean = 1'b0; // Default assignment menjamin variabel selalu memiliki nilai!
        case (sel)
            2'b00:   out_clean = data_in;
            2'b01:   out_clean = ~data_in;
            default: out_clean = 1'b0; // Rangkaian disintesis murni sebagai multiplexer gerbang!
        endcase
    end
endmodule
```""",
            "analysis": r"""- **Aturan Linting RTL & Nol Toleransi Latch**: Standar desain industri semikonduktor (seperti aturan SpyGlass RTL Linting) menetapkan peringatan inferensi latch sebagai *Fatal Error*. Praktik terbaik yang wajib diterapkan adalah memberikan nilai bawaan default (*default assignment*) pada baris paling awal dari setiap blok kombinasi `always @(*)`, atau menggunakan konstruk SystemVerilog modern `always_comb` yang secara otomatis membangkitkan galat kompilasi (*compile error*) jika ada struktur latch yang terbentuk."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul multiplexer 4-ke-1 kombinasional dalam Verilog menggunakan pernyataan `case` dengan penanganan lengkap seluruh kondisi, buktikan bahwa tidak ada latch yang disintesis.
- **Petunjuk Perancangan Arsitektur**:
  - Petakan selector 2-bit `sel` ke 4 input data $D_0, D_1, D_2, D_3$.
  - Tambahkan klausul `default: out = 1'b0;` untuk kepatuhan ketat standar linting.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Evaluasi Seluruh Input*: Uji seluruh kombinasi `sel` dari `00` hingga `11`; verifikasi output mengikuti input terpilih tepat.
  - *Inspeksi Netlist Sintesis*: Pastikan netlist hanya menggunakan sel kombinasional MUX/AOI tanpa elemen level-sensitive latch.
- **Rubrik Penilaian Mandiri**: 40% Sintaks Verilog Kombinasional Bebas Latch Presisi, 30% Kepatuhan Aturan Default Assignment, 30% Verifikasi Seluruh Vektor Kasus Uji.

### Tingkat 2: Menengah
- **Tugas**: Bangun linter statis skrip Python parser AST sederhana untuk kode sumber Verilog yang mendeteksi inferensi latch pada blok `always @(*)` dengan memeriksa apakah semua variabel target yang ditulis memiliki jalur penugasan di setiap cabang percabangan `if-else` pohon sintaks.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun graf kontrol aliran (Control Flow Graph / CFG) dari blok `always`.
  - Verifikasi bahwa setiap lintasan dari entri ke keluar melewati setidaknya satu pernyataan penugasan untuk setiap variabel yang dimodifikasi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Missing Else*: Berikan kode `if (A) Y = B;` tanpa `else`; linter harus membangkitkan peringatan error latch pada variabel $Y$.
  - *Penugasan Default Awal*: Berikan kode dengan inisialisasi awal `Y = 0; if (A) Y = B;`; linter harus mengonfirmasi kode 100% bersih.
- **Rubrik Penilaian Mandiri**: 40% Analisis Jalur Kontrol Aliran CFG Verilog Tepat, 30% Deteksi Akurat Kondisi Latch Tanpa False Positive, 30% Penanganan Variabel Multi-Target.

### Tingkat 3: Mahir
- **Tugas**: Rancang ALU 32-bit parametrik synthesizable dalam SystemVerilog (`always_comb` dan `always_ff`) yang mendukung 16 operasi aritmatika dan logika lengkap (ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU), buktikan kebersihan sintesis menggunakan Yosys open-source synthesis tool, dan verifikasi zero latch inference melalui assertion formal `assert property`.
- **Petunjuk Perancangan Arsitektur**:
  - Gunakan penugasan default di awal blok `always_comb`.
  - Tulis assertion formal SVA (SystemVerilog Assertions) untuk memastikan bahwa output ALU tidak pernah bernilai `X` (undefined) ketika input operasional valid.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Yosys Netlist Inspection*: Jalankan perintah sintesis Yosys; verifikasi bahwa jumlah sel `$_DLATCH_*` tepat bernilai nol.
  - *Shift Negatif Ekstrem*: Uji operasi pergeseran aritmatika kanan (SRA) pada bilangan negatif bertanda; verifikasi penyalinan bit tanda MSB.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur ALU 32-Bit SystemVerilog Lengkap Presisi, 30% Verifikasi Bersih Bebas Latch pada Yosys Synthesis Tool, 30% Assertion Formal Ketiadaan Nilai X."""
    },
    59: {
        "trace": r"""#### Tabel Penelusuran Kontensi Bus Internal FPGA & Pelelehan Jalur Silikon Interkoneksi
| Siklus Jam ($Clk$) | Status Driver Buffer Tri-State 1 | Sinyal Data Driver 1 ($D_1$) | Status Driver Buffer Tri-State 2 | Sinyal Data Driver 2 ($D_2$) | Arus Kontensi Sambungan Bus Silikon ($I_{bus}$) |
|---|---|---|---|---|---|
| Siklus 0 (Normal) | ENABLE ($OE_1 = 1$) | Mengirim Logika HIGH ($3.3\text{ V}$) | DISABLED ($OE_2 = 0$) | Status impedansi tinggi (High-Z) | $0.0\text{ mA}$ (Operasi bus normal) |
| Siklus 1 (Transisi) | DISABLED ($OE_1 = 0$) | High-Z | ENABLE ($OE_2 = 1$) | Mengirim Logika LOW ($0.0\text{ V}$) | $0.0\text{ mA}$ (Transisi aman) |
| Siklus 2 (Cacat Logika)| ENABLE ($OE_1 = 1$) | Mengirim Logika HIGH ($3.3\text{ V}$) | ENABLE ($OE_2 = 1$) | Mengirim Logika LOW ($0.0\text{ V}$) | KEDUA DRIVER AKTIF DENGAN TEGANGAN BERLAWANAN!|
| Hubungan Singkat Silikon| Transistor PMOS menyala penuh | Resistansi internal $R_{on} \approx 20\ \Omega$ | Transistor NMOS menyala penuh | Resistansi internal $R_{on} \approx 20\ \Omega$ | Arus korsleting langsung: $I = \frac{3.3}{40} = 82.5\text{ mA}$! |
| Kaskade Termal Bus Lebar| 32 jalur bus kontensi serempak | Arus total bus: $32 \times 82.5\text{ mA} = 2.64\text{ A}$ | Panas disipasi lokal $> 8.7\text{ W}$ | Suhu logam interconnect tembus $250^\circ\text{C}$| Jalur metallisasi aluminium FPGA meleleh terputus |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kontensi Bus Internal pada Tri-State Buffer FPGA Melelehkan Jalur Metallisasi Silikon",
            "chronology": r"""- **Insiden Kegagalan Perangkat Keras FPGA**: Pada pengujian kartu akselerator PCIe berbasis FPGA Xilinx Virtex, chip FPGA mengalami lonjakan arus catu daya 3,3V yang sangat masif sesaat setelah bitstream konfigurasi dimuat. Suhu permukaan chip melonjak melewati 120°C dalam waktu lima detik dan chip mati permanen dengan resistansi catu daya turun menjadi nol (korsleting internal permanen).
- **Akar Masalah Arsitektur FPGA & Kontensi Bus Tri-State**: Pada chip ASIC tradisional, bus data bersama sering kali dibangun menggunakan buffer tiga keadaan (*tri-state buffers* dengan status impedansi tinggi High-Z). Namun, struktur internal FPGA modern terdiri dari jutaan blok logika terkonfigurasi (CLB) yang saling terhubung melalui matriks saklar perutean statis (*routing switch matrices*), bukan kabel fisik tri-state riil. Ketika perancang memigrasikan kode RTL lama yang menggunakan buffer tri-state internal (`assign bus = (en1) ? data1 : 1'bz; assign bus = (en2) ? data2 : 1'bz;`), kesalahan logika kontrol mengaktifkan kedua sinyal pemungkin (*enable*) secara bersamaan. Driver pertama menarik saluran ke $V_{DD}$ (logika 1), sementara driver kedua menarik saluran ke GND (logika 0). Struktur fisik FPGA mengemulasikan ini dengan dua pasang transistor output yang saling bertolak belakang. Arus hubungan singkat masif (*bus contention current*) mengalir langsung dari rel daya ke ground melintasi saluran perutean silikon yang sangat tipis, membakar transistor saklar perutean FPGA dan melelehkan jalur logam interkoneksi silikon secara ireversibel.""",
            "snippet": r"""```verilog
// Contoh Buruk Bus Tri-State Internal FPGA vs Solusi Multiplexer Modern
module fpga_bus_bad (
    input  wire       en1, en2,
    input  wire [7:0] data1, data2,
    output wire [7:0] bus_internal_bad,
    output wire [7:0] bus_internal_safe
);
    // POLA BERBAHAYA DI FPGA: Bus Tri-State Internal
    // Jika en1 == 1 dan en2 == 1, terjadi kontensi perangkat keras internal!
    assign bus_internal_bad = en1 ? data1 : 8'bzzzz_zzzz;
    assign bus_internal_bad = en2 ? data2 : 8'bzzzz_zzzz;

    // POLA AMAN: Sepenuhnya digantikan oleh Multiplexer MUX
    // Tidak pernah terjadi kontensi fisik; disintesis ke Look-Up Table (LUT)
    assign bus_internal_safe = en1 ? data1 :
                               en2 ? data2 : 8'h00;
endmodule
```""",
            "analysis": r"""- **Prinsip Arsitektur FPGA Modern**: Arsitektur FPGA modern (seperti AMD/Xilinx UltraScale dan Intel Stratix) telah menghapus sepenuhnya elemen tri-state buffer dari kain logika internal (*internal routing fabric*). Elemen tri-state hanya diizinkan dan secara fisik tersedia pada blok pin bantalan antarmuka eksternal (*Input/Output Blocks* / IOB). Seluruh komunikasi bus multi-sumber internal wajib disintesis menggunakan multiplexer pohon berbasis Look-Up Table (LUT) atau bus terdistribusi AXI4/Wishbone."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun modul Look-Up Table (LUT) 4-input dalam Verilog yang dapat dikonfigurasikan dengan tabel kebenaran 16-bit sembarang untuk mengemulasikan fungsi logika Boolean apapun.
- **Petunjuk Perancangan Arsitektur**:
  - Simpan konfigurasi 16-bit ke dalam register parameter `CFG_INIT`.
  - Gunakan 4 bit masukan sebagai indeks seleksi multiplexer 16-ke-1 untuk memilih bit keluaran.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Konfigurasi Gerbang XOR 2-Input*: Set bit konfigurasi yang sesuai; verifikasi fungsi XOR pada masukan.
  - *Konfigurasi Carry Full Adder*: Set tabel kebenaran carry; verifikasi fungsionalitas penambahan bitwise.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur LUT4 Berbasis Multiplexer Presisi, 30% Fleksibilitas Konfigurasi Bitstream INIT, 30% Verifikasi Ekivalensi Logika Berbagai Gerbang.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator penempatan dan perutean (Placement & Routing) sederhana berbasis algoritma Simulated Annealing untuk memetakan graf rangkaian netlist gerbang ke dalam kisi array CLB FPGA 2D, meminimalkan panjang kawat interkoneksi pembatas (*Half-Perimeter Wirelength* / HPWL).
- **Petunjuk Perancangan Arsitektur**:
  - Evaluasi fungsi biaya: $HPWL = \sum_{net} (x_{max} - x_{min} + y_{max} - y_{min})$.
  - Terapkan jadwal pendinginan eksponensial: $T_{k+1} = \alpha T_k$ dengan $\alpha = 0.95$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Jaringan Rantai Sederhana*: Verifikasi bahwa Simulated Annealing menempatkan CLB yang terhubung berurutan pada posisi spasial yang bertetangga.
  - *Konvergensi Biaya*: Buktikan penurunan biaya total HPWL $\ge 50\%$ dibanding penempatan acak awal.
- **Rubrik Penilaian Mandiri**: 40% Solver Simulated Annealing Penempatan CLB Presisi, 30% Formulasi Biaya Interkoneksi HPWL Tepat, 30% Analisis Konvergensi Suhu Pendinginan.

### Tingkat 3: Mahir
- **Tugas**: Rancang interkoneksi bus on-chip AXI4-Lite Crossbar Switch parametrik ($N$-Master ke $M$-Slave) synthesizable dalam SystemVerilog, dengan mekanisme arbitrase Round-Robin yang adil, deteksi konflik alamat tujuan, dan penanganan timeout transaksi yang mencegah penguncian bus jika slave tidak merespons.
- **Petunjuk Perancangan Arsitektur**:
  - Pisahkan saluran alamat baca/tulis dan data baca/tulis sesuai spesifikasi AMBA AXI4-Lite.
  - Terapkan arbiter putaran adil (*Fair Round-Robin Arbiter*) untuk mencegah kelaparan (*starvation*) master prioritas rendah.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Akses Simultan Bersama*: Dua master meminta slave yang sama pada siklus yang sama; verifikasi hibah arbitrase bergantian secara adil tanpa kehilangan data.
  - *Slave Tak Merespons*: Injeksi slave macet tanpa menegaskan `READY`; crossbar harus membangkitkan respon error `DECERR` setelah 256 siklus jam dan membebaskan bus.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Ketat Protokol AMBA AXI4-Lite Handshake Presisi, 30% Algoritma Arbitrase Round-Robin Bebas Starvation, 30% Mekanisme Pemulihan Timeout & Error Reporting."""
    },
    60: {
        "trace": r"""#### Tabel Penelusuran Eksploitasi Perangkat Keras DRAM Rowhammer (CVE-2014-0417)
| Siklus Aktivasi DRAM | Operasi Memori CPU | Alamat Baris Memori Sasaran (Aggressor) | Kebocoran Muatan Kapasitor Sel Tetangga | Status Tegangan Baris Target (Victim) | Mutasi Bit Memori Terlindung Kernel |
|---|---|---|---|---|---|
| Inisialisasi ($t=0$) | Alokasi Halaman RAM | Baris $A$ (Alamat User), Baris $V$ (Kernel Page Table) | Isolasi parit dielektrik normal | Kapasitor penuh ($V_{cap} = 1.2\text{ V}$) | Nilai bit target $= 1$ biner |
| Siklus 1 - 50.000 | Eksekusi instruksi `clflush` | Baris $A$ diaktivasi dan ditutup berulang | Fluktuasi tegangan wordline frekuensi tinggi | Muatan mulai bocor melintasi isolator tipis | Kapasitor baris tetangga meluruh cepat |
| Siklus 150.000 | Akses bolak-balik (Double-Sided)| Baris $A_1$ dan $A_2$ memukul baris $V$ di tengah | Kopling kapasitif parasitik antar-sel DRAM | Tegangan kapasitor turun ke $0.65\text{ V}$ | Mendekati ambang batas switching sense amp |
| Siklus 300.000 | Interval refresh DRAM terlampaui| Pukulan cepat sebelum siklus refresh sempat tiba | Muatan tersisa terkuras habis | Tegangan anjlok ke $0.20\text{ V}$ ($< V_{ref}$) | BITHLIP TERJADI! Nilai bit berubah $1 \to 0$! |
| Dampak Keamanan | Penyerang memeriksa memori | Bit izin tabel halaman kernel terbalik | Status halaman berubah dari Read-Only ke Writable | Akses root diperoleh tanpa password! | Kernel dieksploitasi penuh dari mode unprivileged |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Eksploitasi Perangkat Keras DRAM Rowhammer Membalik Bit Kernel Tanpa Hak Akses (2014)",
            "chronology": r"""- **Penemuan Kerentanan Silikon Global**: Pada tahun 2014, peneliti dari Carnegie Mellon University dan Google Project Zero membuktikan bahwa kelemahan fisik pada transistor memori DRAM modern memungkinkan program tingkat pengguna (*unprivileged user process*) membalik bit data pada halaman memori milik sistem operasi atau pengguna lain tanpa mengeksploitasi cacat perangkat lunak satupun.
- **Akar Masalah Fisika Memori Semikonduktor & Kopling Kapasitif**: Untuk meningkatkan kapasitas memori RAM menjadi gigabit pada chip silikon kecil, ukuran sel penyimpanan DRAM (1 transistor, 1 kapasitor / 1T-1C) dipipihkan hingga skala nanometer, menempatkan jutaan kawat jalur baris (*wordlines*) saling berdampingan dalam jarak sangat rapat. Ketika sebuah baris memori diakses berulang kali dengan kecepatan jutaan kali per detik (menggunakan instruksi perakitan pembersih cache CPU `clflush` untuk melewati cache prosesor), tegangan listrik pada wordline baris agresor (*aggressor row*) dihidupkan dan dimatikan secara ekstrem. Kopling elektromagnetik parasitik dan pergerakan muatan terakselerasi membocorkan elektron dari kapasitor sel memori tetangga (*victim row*). Jika kebocoran terjadi lebih cepat daripada interval penyegaran otomatis DRAM (siklus refresh standar 64 ms), kapasitor sel tetangga kehilangan muatannya sebelum sempat di-refresh, menyebabkan bit biner terbalik secara spontan (*bitflip* dari 1 menjadi 0 atau sebaliknya). Penyerang memanfaatkan ini untuk membalik bit izin pada *Page Table Entry* (PTE), memperoleh hak akses tulis ke memori kernel fisik.""",
            "snippet": r"""```c
// Rekonstruksi Proof-of-Concept Perangkat Keras DRAM Rowhammer (Assembly x86_64)
#include <stdio.h>
#include <stdint.h>

void execute_double_sided_rowhammer(volatile uint32_t *aggressor1, volatile uint32_t *aggressor2, int iterations) {
    // Membaca baris agresor 1 dan 2 secara bergantian sembari membuang cache line
    // Memaksa pengontrol memori membuka dan menutup baris DRAM (ACTIVATE/PRECHARGE) jutaan kali
    for (int i = 0; i < iterations; i++) {
        // 1. Baca data dari agresor 1 (paksa aktivasi baris DRAM)
        uint32_t val1 = *aggressor1;
        // 2. Baca data dari agresor 2
        uint32_t val2 = *aggressor2;
        
        // 3. Bersihkan baris memori dari L1/L2/L3 cache CPU menggunakan clflush
        asm volatile (
            "clflush (%0)\n\t"
            "clflush (%1)\n\t"
            :
            : "r" (aggressor1), "r" (aggressor2)
            : "memory"
        );
    }
}
```""",
            "analysis": r"""- **Solusi Mitigasi Perangkat Keras**: Bencana Rowhammer memaksa standardisasi JEDEC merevisi arsitektur DRAM DDR4 dan DDR5 dengan mengintegrasikan fitur mitigasi perangkat keras: 1) *Targeted Row Refresh* (TRR) di mana chip DRAM mendeteksi baris yang diakses secara agresif dan secara otomatis menyegarkan baris tetangganya di luar siklus normal; 2) Penggunaan memori dengan kode koreksi kesalahan *Error-Correcting Code* (ECC) yang mampu mendeteksi dan mengoreksi bitflip tunggal secara transparan."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun fungsi penyandi dan pemeriksa paritas matriks Hamming Code (7, 4) dalam Python yang mampu mendeteksi dan mengoreksi kesalahan bitflip tunggal (Single Error Correction / SEC) pada blok data 4-bit.
- **Petunjuk Perancangan Arsitektur**:
  - Matriks Generator $G_{4 \times 7}$ dan Matriks Pemeriksa Paritas $H_{3 \times 7}$.
  - Hitung vektor sindrom $S = r \cdot H^T$; jika $S \ne 0$, vektor sindrom menunjukkan indeks kolom bit yang mengalami kesalahan.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Data Normal*: Data 4-bit `1011`; verifikasi kodeword 7-bit yang dihasilkan.
  - *Injeksi Bitflip*: Ubah bit ke-5; buktikan bahwa vektor sindrom mengidentifikasi posisi bit 5 dan mengoreksi nilainya kembali ke data asli.
- **Rubrik Penilaian Mandiri**: 40% Formulasi Matriks Generator & Paritas Hamming Tepat, 30% Algoritma Perhitungan Sindrom & Koreksi Bitflip Presisi, 30% Verifikasi Fungsionalitas Data Uji.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator siklus refresh DRAM dan estimasi probabilitas kegagalan retensi muatan kapasitor sel terhadap temperatur operasi silikon berdasarkan hukum kebocoran arus deplesi sambungan PN eksponensial.
- **Petunjuk Perancangan Arsitektur**:
  - Muatan kapasitor: $Q(t) = Q_0 - \int I_{leak}(T) dt$ dengan arus bocor mengganda setiap kenaikan $10^\circ\text{C}$ ($I_{leak} \propto 2^{\Delta T / 10}$).
  - Simulasikan interval penyegaran standar $t_{ref} = 64\text{ ms}$ pada $25^\circ\text{C}$ vs $85^\circ\text{C}$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Suhu Kamar $25^\circ\text{C}$*: Muatan tersisa saat siklus refresh tiba $\ge 85\% Q_0$ (sangat aman).
  - *Suhu Tinggi $95^\circ\text{C}$*: Muatan terkuras di bawah ambang deteksi Sense Amplifier sebelum 64 ms (memerlukan adaptive refresh rate 32 ms).
- **Rubrik Penilaian Mandiri**: 40% Model Ketergantungan Suhu Kebocoran Muatan Eksponensial Tepat, 30% Simulasi Siklus Refresh & Sense Amp Sensing, 30% Evaluasi Batas Waktu Retensi Data.

### Tingkat 3: Mahir
- **Tugas**: Rancang modul pengontrol memori perangkat keras (Memory Controller) dengan logika mitigasi Targeted Row Refresh (TRR) berbasis penjejak baris agresif menggunakan algoritma Space-Saving atau Misra-Gries Stream Summary, identifikasi baris memori yang frekuensi aksesnya melampaui batas ambang bahaya Rowhammer, dan jadwalkan penyegaran preventif baris korban secara instan.
- **Petunjuk Perancangan Arsitektur**:
  - Pantau aliran perintah aktivasi DRAM `ACTIVATE` baris secara streaming dalam memori terikat kecil (16 register penjejak).
  - Jika sebuah baris diakses $> K$ kali dalam jendela refresh saat ini, bangkitkan perintah penyegaran khusus untuk baris $Row + 1$ dan $Row - 1$.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Serangan Rowhammer Terdistribusi*: Simulasikan penyerang yang memukul 10 baris berbeda secara acak; buktikan algoritma TRR mendeteksi seluruh baris agresor utama.
  - *Zero False Starvation*: Operasi refresh normal tidak boleh terganggu dengan latensi tambahan $\le 2\%$.
- **Rubrik Penilaian Mandiri**: 40% Implementasi Algoritma Streaming Stream-Summary Presisi, 30% Logika Penjadwalan Perintah Refresh Target TRR Tepat, 30% Pembuktian Penekanan Bitflip di Bawah Beban Serangan."""
    },
    61: {
        "trace": r"""#### Tabel Penelusuran Ketiadaan Koherensi Instruction Cache (I-Cache) pada Kompilator JIT
| Tahap Eksekusi JIT | Komponen Sistem / Alamat Memori | Aksi Penulisan / Pembacaan CPU | Status Data Cache (D-Cache L1) | Status Instruction Cache (I-Cache L1) | Instruksi yang Dieksekusi CPU Core |
|---|---|---|---|---|---|
| Kompilasi JIT | Compiler Runtime (Ring 3) | Emisi kode mesin baru ke memori RAM | Menulis kode biner baru | I-Cache masih memuat data kode lama | Belum melompat ke fungsi baru |
| Penulisan Selesai | Buffer Alamat `0x4000_1000` | Penulisan selesai di memori data | Baris cache berstatus DIRTY | Kosong atau memuat instruksi usang | Siap mengeksekusi fungsi |
| Pemanggilan Fungsi | CPU melompat: `JMP 0x4000_1000` | Fetch unit mengambil instruksi | Menahan instruksi baru di D-Cache | I-Cache Miss / Hit kode usang sebelumnya! | CPU mengeksekusi instruksi dari I-Cache! |
| Ketiadaan Koherensi | Arsitektur Modified Harvard | D-Cache dan I-Cache terpisah fisik | D-Cache tidak mem-flush data ke RAM | I-Cache tidak meng-invalidasi entri | CPU mengeksekusi instruksi usang / byte nol sampah! |
| Dampak Crash | CPU menjumpai instruksi ilegal | Instruksi biner terkorupsi dieksekusi | - | Alamat return rusak | Illegal Instruction Exception / SIGSEGV crash! |
| Dengan Flush Sinkron | Instruksi `fence.i` / clear cache | D-Cache di-flush ke PoU; I-Cache di-invalidate | Data sinkron di RAM fisik | I-Cache memuat ulang instruksi baru | Fungsi JIT berjalan mulus berkecepatan tinggi! |""",
        "postmortem": {
            "title": "Studi Kasus Kegagalan Nyata: Kegagalan Koherensi Instruction Cache (I-Cache) pada Kompilator JIT Mesin Virtual",
            "chronology": r"""- **Insiden Kegagalan Mesin Virtual JIT**: Saat melakukan porting mesin eksekusi JavaScript V8 / Java JVM ke prosesor arsitektur ARM64 dan RISC-V terbaru, perancang mendapati browser dan server web mengalami crash mendadak `SIGILL` (Illegal Instruction) atau `SIGSEGV` secara sporadis setiap kali fungsi kode yang baru saja dikompilasi oleh Just-In-Time (JIT) compiler dipanggil untuk pertama kali.
- **Akar Masalah Model Arsitektur Komputer & Modified Harvard Architecture**: Sebagian besar prosesor modern menerapkan arsitektur Modified Harvard: CPU memiliki dua cache L1 fisik terpisah—L1 Data Cache (D-Cache) untuk membaca dan menulis variabel, serta L1 Instruction Cache (I-Cache) untuk mengambil instruksi mesin yang akan dieksekusi. Karena kode mesin dianggap tidak pernah dimodifikasi saat eksekusi normal (*read-only*), perangkat keras CPU tidak menerapkan koherensi cache otomatis antara D-Cache dan I-Cache demi efisiensi kecepatan. Ketika kompilator JIT menghasilkan kode biner baru, ia menulis instruksi tersebut ke memori laksana data biasa; kode baru ini tertahan di dalam D-Cache berstatus *dirty*. Ketika CPU segera melompat ke alamat memori tersebut untuk mengeksekusinya, unit instruksi CPU membaca instruksi dari I-Cache atau RAM fisik yang masih berisi instruksi usang atau byte nol sampah. Ketiadaan instruksi sinkronisasi penyelarasan memori eksplisit menyebabkan CPU mengeksekusi data sampah dan memicu crash seketika.""",
            "snippet": r"""```c
// Kode Kompilator JIT C: Sinkronisasi Wajib D-Cache dan I-Cache
#include <stdio.h>
#include <sys/mman.h>
#include <string.h>

typedef int (*jit_func_t)(int);

jit_func_t compile_and_flush_jit() {
    // 1. Alokasi halaman memori yang dapat ditulis dan dieksekusi
    void *mem = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
                     MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
                     
    // 2. Tulis kode mesin (misal fungsi sederhana return x + 1 dalam ARM64 atau x86)
    unsigned char code[] = {
        0xb8, 0x01, 0x00, 0x00, 0x00, // mov eax, 1 (x86_64)
        0xc3                          // ret
    };
    memcpy(mem, code, sizeof(code));

    // 3. KRUSIAL: Pada ARM/RISC-V, sinkronisasi cache wajib dipanggil eksplisit!
    // Memaksa D-Cache menulis ke memori dan membersihkan I-Cache
    #if defined(__GNUC__)
    __builtin___clear_cache((char *)mem, (char *)mem + sizeof(code));
    #endif
    
    // Pada RISC-V assembly: perintah eksplisit `fence.i`
    // Pada ARM64 assembly: `dc cvau, reg` (clean D-cache) lalu `ic ivau, reg` (invalidate I-cache)

    return (jit_func_t)mem;
}
```""",
            "analysis": r"""- **Prinsip Point of Unification (PoU)**: Dalam arsitektur sistem operasi dan kompilator modern, transisi dari penulisan data ke eksekusi instruksi mewajibkan pemanggilan sistem sinkronisasi *Point of Unification*. Sistem operasi menyediakan antarmuka seperti `sys_cacheflush()` di Linux atau instruksi arsitektur khusus seperti `fence.i` (RISC-V) dan `ISB / DSB` (ARM) untuk menjamin bahwa seluruh modifikasi data telah dikomit ke titik penyatuan memori sebelum pipa dekoder instruksi memuat instruksi baru."""
        },
        "exercise": r"""### Tingkat 1: Dasar
- **Tugas**: Bangun simulator mesin von Neumann sederhana berbasis register 8-bit dalam Python dengan memori terpadu (Unified Memory) 256 byte, buktikan konsep kode modifikasi diri (*Self-Modifying Code*) di mana program menulis instruksi baru ke memorinya sendiri dan kemudian mengeksekusinya.
- **Petunjuk Perancangan Arsitektur**:
  - Siklus Fetch-Decode-Execute dengan Program Counter ($PC$) dan Akumulator ($ACC$).
  - Eksekusi program yang memodifikasi opcode instruksi berikutnya di alamat memori $PC+2$ sebelum melewatinya.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Modifikasi Diri Berhasil*: Instruksi `ADD 5` dimodifikasi menjadi `SUB 5` saat berjalan; verifikasi hasil akumulator berubah sesuai instruksi baru.
  - *Batas Memori*: Eksekusi melintasi batas 255 byte wrap-around kembali ke alamat 0 dengan aman.
- **Rubrik Penilaian Mandiri**: 40% Simulator Siklus Instruksi Von Neumann Presisi, 30% Pembuktian Eksekusi Self-Modifying Code Tepat, 30% Penanganan Status Register & Flags.

### Tingkat 2: Menengah
- **Tugas**: Implementasikan simulator hierarki cache dua-tingkat (L1 Data Cache dan L1 Instruction Cache terpisah / Split Harvard) yang melacak status koherensi baris cache (Valid, Dirty, Invalid) dan mendeteksi kondisi eksekusi data basi (*stale instruction execution bug*) jika fungsi penulisan memori tidak diiringi operasi pembersihan cache.
- **Petunjuk Perancangan Arsitektur**:
  - Modelkan ukuran blok cache 64-byte dengan pemetaan asosiatif set ganda.
  - Bangun metode `write_data(addr, val)` yang memperbarui D-Cache dan menandai baris sebagai DIRTY.
  - Bangun metode `fetch_instruction(addr)` yang membaca dari I-Cache; bangkitkan peringatan bahaya jika alamat tersebut berstatus DIRTY di D-Cache namun I-Cache belum di-invalidate.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Deteksi Inkoherensi JIT*: Tulis kode baru ke RAM; panggil fetch tanpa `flush()`; simulator wajib melaporkan pelanggaran koherensi instruksi.
  - *Siklus Sinkronisasi Lengkap*: Jalankan `flush_and_invalidate()`; buktikan fetch berhasil memuat instruksi terbaru.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Split L1 I-Cache & D-Cache Tepat, 30% Deteksi Otomatis Kondisi Stale Instruction Hazard, 30% Verifikasi Operasi Penyelarasan Point of Unification.

### Tingkat 3: Mahir
- **Tugas**: Rancang mesin kompilasi mikro JIT assembler runtime untuk subset instruksi RISC-V 32-bit (RV32I) dalam C/Rust yang secara dinamis menyusun bytecode operasi aritmatika menjadi kode mesin biner di memori eksekusi, lengkap dengan eksekusi urutan barrier memori perangkat keras (`fence` dan `fence.i`) yang mematuhi standar memori model RISC-V Weak Memory Ordering (RVWMO).
- **Petunjuk Perancangan Arsitektur**:
  - Alokasikan memori halaman executable menggunakan `mprotect()` atau `VirtualProtect()`.
  - Terjemahkan ekspresi aritmatika stack menjadi deretan instruksi biner RV32I (`addi`, `add`, `sub`).
  - Sisipkan instruksi sinkronisasi instruksi `fence.i` sebelum memanggil fungsi melalui penunjuk fungsi.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Eksekusi Fungsi Majemuk*: Kompilasi ekspresi $(x \times 3) - 7$; eksekusi untuk $x = 10$; buktikan hasil keluaran tepat $23$.
  - *Verifikasi Barrier Memori*: Buktikan secara empiris bahwa pemanggilan tanpa memory barrier gagal pada arsitektur perangkat keras non-koheren.
- **Rubrik Penilaian Mandiri**: 40% Emitor Kode Biner RISC-V RV32I JIT Presisi, 30% Kepatuhan Ketat Barrier Memori RVWMO `fence.i`, 30% Manajemen Izin Halaman Memori Virtual Dinamis."""
    }
}
