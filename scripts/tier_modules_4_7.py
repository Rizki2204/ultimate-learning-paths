# scripts/tier_modules_4_7.py
"""
Rich generator implementations for Tier 4, 5, 6, and 7:
Computer Architecture, Embedded Systems, Computer Science Core, and Linux OS Internals.
"""

def _gen_tier_4(topic_id, slug, full_title):
    ca_catalog = {
        53: {
            "intuition": "Aljabar Boolean adalah matematika dari saklar lampu. Jika Anda memiliki dua saklar yang disusun berseri di kabel yang sama, lampu hanya menyala jika saklar A DAN saklar B ditutup (Gerbang AND). Jika disusun paralel berdampingan, lampu menyala jika saklar A ATAU saklar B ditutup (Gerbang OR). Dari dua aturan sederhana ini, kita dapat membangun seluruh komputer digital di dunia!",
            "theory": """
Aksioma Aljabar Boolean Huntington:
1. Penutupan (*Closure*): $a + b \\in \\mathcal{B}$, $a \\cdot b \\in \\mathcal{B}$
2. Elemen Identitas: $a + 0 = a$, $a \\cdot 1 = a$
3. Komutatif: $a + b = b + a$, $a \\cdot b = b \\cdot a$
4. Distributif: $a \\cdot (b + c) = (a \\cdot b) + (a \\cdot c)$, $a + (b \\cdot c) = (a + b) \\cdot (a + c)$
5. Komplemen: $a + a' = 1$, $a \\cdot a' = 0$

Hukum De Morgan:
$$(A \\cdot B)' = A' + B'$$
$$(A + B)' = A' \\cdot B'$$
Penyederhanaan Peta Karnaugh (K-Map) mengelompokkan minterm $2^k$ yang berdekatan menggunakan pengkodean Gray Code (hanya 1 bit berubah per langkah tetangga) untuk meminimalkan jumlah gerbang logika.
""",
            "internals": "Setiap fungsi Boolean dapat direalisasikan hanya dengan gerbang universal NAND atau NOR. Pada level CMOS transistor fisik, gerbang NAND 2-input diimplementasikan dengan 2 PMOS paralel di pull-up network dan 2 NMOS seri di pull-down network.",
            "code_block": """```verilog
// Modul Verilog Gerbang Universal NAND dan Dekomposisi Fungsi Logika
module universal_logic (
    input wire a,
    input wire b,
    output wire out_nand,
    output wire out_and,
    output wire out_or
);
    // Gerbang dasar NAND
    assign out_nand = ~(a & b);
    
    // De Morgan: AND(a, b) = NOT(NAND(a, b))
    assign out_and = ~out_nand;
    
    // De Morgan: OR(a, b) = NAND(NOT(a), NOT(b))
    assign out_or = ~(~a & ~b);
endmodule
```""",
            "pitfalls": "Mengabaikan bahaya statis (*static hazard*) dan dinamik (*dynamic hazard*) pada rangkaian logika kombinasi: perbedaan tunda propagasi (*propagation delay*) antar jalur dapat memicu glitch tegangan palsu sesaat.",
            "exercises": "Level 1: Sederhanakan fungsi $F(A,B,C) = \\sum m(1,3,5,7)$ menggunakan aljabar Boolean murni. Level 2: Buat K-Map 4-variabel dan turunkan persamaan Product-of-Sums (POS) teringkas. Level 3: Implementasikan algoritma Quine-McCluskey di Python untuk menyederhanakan fungsi logika hingga 8 variabel.",
            "references": "- Mano, M. M., & Ciletti, M. D. (2018). *Digital Design: With an Introduction to the Verilog HDL*. Pearson.\n- Harris, D., & Harris, S. (2012). *Digital Design and Computer Architecture*. Morgan Kaufmann."
        },
        62: {
            "intuition": "Instruction Set Architecture (ISA) adalah buku kamus kontrak perjanjian resmi antara software programmer dan arsitek hardware chip. Software programmer menyusun instruksi assembly (seperti ADD, LOAD, JUMP), dan prosesor berjanji akan mengeksekusi instruksi tersebut dengan benar tanpa programmer perlu tahu bagaimana kabel transistor di dalamnya dirangkai.",
            "theory": """
Klasifikasi Arsitektur ISA:
1. **CISC (Complex Instruction Set Computer - x86-64)**:
   - Instruksi dengan panjang bervariasi (1 s/d 15 bytes pada x86).
   - Mode pengalamatan memori kaya (*register-memory, memory-memory*).
   - Menghemat ukuran biner dengan instruksi kompleks berkode mikro (*microcode*).
2. **RISC (Reduced Instruction Set Computer - ARM64, RISC-V)**:
   - Panjang instruksi tetap (32-bit standar).
   - Arsitektur *Load/Store* murni (operasi aritmatika hanya terjadi antar register).
   - Eksekusi seragam ramah pipeline perangkat keras.

Format Instruksi Standar RISC-V (RV32I):
- R-Type: Operasi register-register (ADD, SUB, SLL, SLT, XOR, SRL, SRA, OR, AND)
- I-Type: Operasi immediate dan load (ADDI, LW, JALR)
- S-Type: Operasi store (SW, SB, SH)
- B-Type: Percabangan kondisional (BEQ, BNE, BLT, BGE)
- U-Type: Immediate tingkat atas 20-bit (LUI, AUIPC)
- J-Type: Lompatan tak-bersyarat (JAL)
""",
            "internals": "Prosesor CISC modern (Intel Core, AMD Zen) secara internal menerjemahkan instruksi x86 yang rumit menjadi rangkaian instruksi sederhana mirip RISC yang disebut **Micro-operations ($\\\\mu$ops)** melalui decoder hardware berkecepatan tinggi sebelum masuk ke pipeline eksekusi.",
            "code_block": """```assembly
# Assembly RISC-V (RV64I): Fungsi iteratif menghitung Faktorial
# Input: register a0 = n
# Output: register a0 = n!

.globl factorial
factorial:
    addi    sp, sp, -16         # Alokasi stack frame
    sd      ra, 8(sp)           # Simpan return address
    li      t0, 1               # t0 = accumulator hasil = 1
    
loop_start:
    blez    a0, loop_end        # Jika n <= 0, selesai
    mul     t0, t0, a0          # t0 = t0 * n
    addi    a0, a0, -1          # n = n - 1
    j       loop_start

loop_end:
    mv      a0, t0              # Kembalikan hasil di register a0
    ld      ra, 8(sp)           # Restore return address
    addi    sp, sp, 16          # Deallokasi stack frame
    ret                         # Lompat kembali ke caller (jalr zero, ra, 0)
```""",
            "pitfalls": "Mengasumsikan instruksi RISC selalu lebih cepat dari CISC. Pada kenyataannya, biner RISC memiliki *code density* lebih rendah (butuh lebih banyak instruksi untuk tugas yang sama), yang dapat membebani kapasitas Instruction Cache L1 jika tidak menggunakan ekstensi instruksi padat (seperti RISC-V compressed instruction extension 'C').",
            "exercises": "Level 1: Terjemahkan potongan kode loop C sederhana ke assembly RISC-V 32-bit. Level 2: Buat parser biner RISC-V R-Type decoder dalam Python untuk mengekstrak opcode, rd, funct3, rs1, rs2, dan funct7. Level 3: Rancang ekstensi ISA kustom 32-bit untuk akselerasi enkripsi AES atau perkalian matriks 4x4.",
            "references": "- Patterson, D. A., & Hennessy, J. L. (2020). *Computer Organization and Design RISC-V Edition*. Morgan Kaufmann.\n- Waterman, A., & Asanović, K. (2019). *The RISC-V Instruction Set Manual, Volume I: User-Level ISA*."
        }
    }
    if topic_id in ca_catalog:
        return ca_catalog[topic_id]
    return _build_generic_systems(topic_id, slug, full_title, "Computer Engineering & Arsitektur Komputer")

def _gen_tier_5(topic_id, slug, full_title):
    emb_catalog = {
        72: {
            "intuition": "Dalam pemrograman aplikasi desktop atau web, jika Anda ingin menyalakan lampu, Anda memanggil API sistem operasi. Namun dalam pemrograman Bare-Metal di mikrokontroler, tidak ada sistem operasi sama sekali! Anda berbicara langsung dengan kabel silikon: Anda menulis angka biner 1 ke alamat memori fisik tertentu (misal 0x40021018), dan seketika pin tembaga nomor 13 di chip Anda mengeluarkan tegangan 3.3 Volt dan menyalakan lampu LED di dunia nyata!",
            "theory": """
Prinsip Memory-Mapped I/O (MMIO):
Register perangkat keras periferi dipetakan ke ruang alamat memori CPU yang sama dengan RAM.
Manipulasi bitwise register hardware:
- Set bit ke-n (menyalakan): `REG |= (1U << n);`
- Clear bit ke-n (mematikan): `REG &= ~(1U << n);`
- Toggle bit ke-n (membalik): `REG ^= (1U << n);`
- Periksa status bit ke-n: `if (REG & (1U << n)) { ... }`

Kata Kunci `volatile` dalam Bahasa C/C++:
Menginstruksikan kompiler bahwa nilai variabel dapat berubah kapan saja di luar kendali alur kode software (misalnya diubah oleh interupsi hardware atau periferal DMA), sehingga kompiler dilarang keras mengoptimasi pembacaan memori ke dalam register CPU (*caching register*).
""",
            "internals": "Tanpa kata kunci `volatile`, loop polling status hardware `while (!(*STATUS_REG & READY_BIT));` akan dioptimasi oleh GCC dengan flag `-O2` menjadi pembacaan tunggal ke register CPU lalu menjadi infinite loop `while (!r0);`, menyebabkan sistem membeku (hang) selamanya.",
            "code_block": """```c
#include <stdint.h>

// Definisi Register STM32F4 (Cortex-M4): GPIO Port D
#define RCC_AHB1ENR     (*(volatile uint32_t *)(0x40023800 + 0x30))
#define GPIOD_MODER     (*(volatile uint32_t *)(0x40020C00 + 0x00))
#define GPIOD_ODR       (*(volatile uint32_t *)(0x40020C00 + 0x14))
#define GPIOD_BSRR      (*(volatile uint32_t *)(0x40020C00 + 0x18))

#define LED_PIN         12 // PD12 (Green LED on Discovery Board)

void delay_cycles(volatile uint32_t count) {
    while (count--) {
        __asm__("nop"); // Hindari optimasi penghapusan loop
    }
}

int main(void) {
    // 1. Aktifkan Clock Peripheral GPIOD di modul RCC
    RCC_AHB1ENR |= (1U << 3); // Bit 3 mengontrol GPIOD
    
    // 2. Konfigurasi PD12 sebagai General Purpose Output (Mode 01)
    GPIOD_MODER &= ~(3U << (LED_PIN * 2)); // Bersihkan bit mode lama
    GPIOD_MODER |= (1U << (LED_PIN * 2));  // Set mode output
    
    while (1) {
        // Set bit atomic via BSRR (Menyalakan LED)
        GPIOD_BSRR = (1U << LED_PIN);
        delay_cycles(1000000);
        
        // Reset bit atomic via BSRR (Mematikan LED)
        GPIOD_BSRR = (1U << (LED_PIN + 16));
        delay_cycles(1000000);
    }
    return 0;
}
```""",
            "pitfalls": "Menggunakan read-modify-write (`ODR |= (1 << pin)`) pada register output di lingkungan multithreading atau interrupt: operasi ini tidak atomik! Jika interupsi terjadi tepat di antara pembacaan dan penulisan, bit pin lain akan tertimpa. Solusi standar: selalu gunakan register BSRR (*Bit Set/Reset Register*) yang atomik pada hardware.",
            "exercises": "Level 1: Konfigurasikan pin GPIO input dengan pull-up resistor dan baca status push-button. Level 2: Implementasikan driver ring-buffer berbasis pointer volatile untuk menampung byte yang masuk dari UART tanpa packet drop. Level 3: Porting bare-metal GPIO driver dari C ke Rust menggunakan `core::ptr::write_volatile` tanpa runtime std.",
            "references": "- Yiu, J. (2013). *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*. Newnes.\n- STMicroelectronics (2021). *RM0090 Reference Manual: STM32F405/415, STM32F407/417*."
        },
        84: {
            "intuition": "Jika mikrokontroler Anda sedang sibuk menghitung angka matematika yang rumit selama 1 detik, bagaimana ia bisa merespons seketika tombol rem darurat yang ditekan oleh manusia dalam waktu 1 milidetik? Sebuah Real-Time Operating System (RTOS) bertindak seperti komandan militer berdisiplin tinggi: ia membagi program menjadi tugas-tugas kecil (tasks), dan segera menghentikan tugas yang kurang penting saat tugas darurat berprioritas tinggi tiba!",
            "theory": """
Anatomi Task Control Block (TCB) & Context Switching:
Setiap thread/task memiliki ruang stack mandiri di RAM.
Ketika scheduler melakukan Context Switch (via interupsi PendSV pada ARM Cortex-M):
1. Simpan konteks register task saat ini ($R0-R12, LR, PC, xPSR$) ke stack task lama.
2. Simpan pointer stack ($SP$) ke dalam struct TCB task lama.
3. Muat pointer stack ($SP$) dari TCB task prioritas tertinggi berikutnya.
4. Restore register task baru dari stack-nya dan instruksikan CPU melanjutkan eksekusi.

Bahaya Klasik: **Priority Inversion**
Kondisi di mana task berprioritas rendah ($L$) mengunci mutex yang dibutuhkan task berprioritas tinggi ($H$), sementara task prioritas menengah ($M$) merebut CPU dari $L$, secara tidak langsung menunda $H$ dalam waktu tak terduga.
Solusi: Protokol **Priority Inheritance** (prioritas task $L$ dinaikkan sementara menyamai prioritas $H$ selama memegang mutex).
""",
            "internals": "Pada misi Mars Pathfinder NASA (1997), wahana antariksa mengalami restart berulang kali di permukaan Mars akibat Priority Inversion pada VxWorks RTOS antara task transmisi data berprioritas rendah dan task navigasi kritis. Masalah diselesaikan dari jarak jauh dari Bumi dengan mengaktifkan flag Priority Inheritance pada mutex.",
            "code_block": """```c
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

SemaphoreHandle_t xResourceMutex;

void vEmergencyTask(void *pvParameters) {
    for (;;) {
        // Menunggu sinyal rem darurat (blokir tanpa konsumsi siklus CPU)
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);
        
        // Eksekusi rem seketika dengan prioritas tertinggi
        xSemaphoreTake(xResourceMutex, portMAX_DELAY);
        // Aktifkan aktuator pengereman
        xSemaphoreGive(xResourceMutex);
    }
}

void vTelemetryTask(void *pvParameters) {
    for (;;) {
        xSemaphoreTake(xResourceMutex, portMAX_DELAY);
        // Mengirim data telemetri berkala
        xSemaphoreGive(xResourceMutex);
        vTaskDelay(pdMS_TO_TICKS(100)); // Delay non-blocking
    }
}

int main(void) {
    // Inisialisasi Mutex dengan Priority Inheritance bawaan FreeRTOS
    xResourceMutex = xSemaphoreCreateMutex();
    
    xTaskCreate(vEmergencyTask, "EMERGENCY", 512, NULL, configMAX_PRIORITIES - 1, NULL);
    xTaskCreate(vTelemetryTask, "TELEMETRY", 512, NULL, tskIDLE_PRIORITY + 1, NULL);
    
    // Mulai RTOS Scheduler
    vTaskStartScheduler();
    
    for (;;); // Tidak akan pernah sampai ke sini
}
```""",
            "pitfalls": "Memanggil API standar FreeRTOS dari dalam Interrupt Service Routine (ISR): memanggil `xQueueSend()` di dalam ISR akan menyebabkan crash kernel fatal; Anda WAJIB menggunakan varian ISR yang aman, yaitu `xQueueSendFromISR()` beserta flag `portYIELD_FROM_ISR()`.",
            "exercises": "Level 1: Buat dua task FreeRTOS yang menyalakan dua LED dengan frekuensi kedipan berbeda menggunakan `vTaskDelay()`. Level 2: Implementasikan producer-consumer queue inter-task communication dengan zero-copy (melewatkan pointer buffer). Level 3: Rancang mini RTOS preemptive cooperative scheduler sendiri dari nol menggunakan bahasa C dan assembly PendSV pada mikrokontroler Cortex-M.",
            "references": "- Barry, R. (2016). *Mastering the FreeRTOS Real Time Kernel: A Hands-On Tutorial Guide*. Real Time Engineers Ltd.\n- Ganssle, J. (2008). *The Firmware Handbook*. Newnes."
        }
    }
    if topic_id in emb_catalog:
        return emb_catalog[topic_id]
    return _build_generic_systems(topic_id, slug, full_title, "Embedded Systems, Firmware Bare-Metal & RTOS")

def _gen_tier_6(topic_id, slug, full_title):
    cs_catalog = {
        93: {
            "intuition": "Jika program Anda memproses 10 data dalam 1 detik, berapa lama waktu yang dibutuhkan jika datanya melonjak menjadi 1 juta? Jika program Anda berjalan dalam $O(N)$, ia hanya butuh 100 detik. Namun jika algoritma Anda berantakan dan berjalan dalam $O(N^2)$, program Anda akan berjalan selama 11 hari nonstop! Notasi Big-O adalah skala Richter dalam rekayasa komputer untuk mengukur apakah kode Anda akan selamat atau meledak saat data dunia nyata datang bertubi-tubi.",
            "theory": """
Definisi Formal Notasi Asimtotik:
1. **Big-O (Batas Atas Asimtotik)**:
   $$f(n) = O(g(n)) \\iff \\exists c > 0, n_0 > 0 \\text{ sedemikian sehingga } \\forall n \\ge n_0, \\quad 0 \\le f(n) \\le c \\cdot g(n)$$
2. **Big-Omega (Batas Bawah Asimtotik)**:
   $$f(n) = \\Omega(g(n)) \\iff \\exists c > 0, n_0 > 0 \\text{ sedemikian sehingga } \\forall n \\ge n_0, \\quad 0 \\le c \\cdot g(n) \\le f(n)$$
3. **Big-Theta (Batas Ketat Asimtotik)**:
   $$f(n) = \\Theta(g(n)) \\iff f(n) = O(g(n)) \\land f(n) = \\Omega(g(n))$$

Teorema Master untuk Relasi Rekurensi Divide & Conquer:
$$T(n) = a \\cdot T(n/b) + f(n), \\quad a \\ge 1, b > 1$$
Bandingkan $f(n)$ dengan $n^{\\log_b a}$:
- Kasus 1: $f(n) = O(n^{\\log_b a - \\epsilon}) \\implies T(n) = \\Theta(n^{\\log_b a})$
- Kasus 2: $f(n) = \\Theta(n^{\\log_b a} \\log^k n) \\implies T(n) = \\Theta(n^{\\log_b a} \\log^{k+1} n)$
- Kasus 3: $f(n) = \\Omega(n^{\\log_b a + \\epsilon}) \\land a f(n/b) \\le c f(n) \\implies T(n) = \\Theta(f(n))$
""",
            "internals": "Amortized Analysis mengukur rata-rata biaya operasi terburuk sepanjang rangkaian eksekusi panjang. Contoh klasik: `std::vector::push_back` membutuhkan alokasi memori $O(N)$ saat kapasitas array habis, tetapi karena kapasitas digandakan secara eksponensial ($2\\times$), biaya teramortisasi setiap penambahan elemen tetap murni $\\Theta(1)$.",
            "code_block": """```python
import time
import matplotlib.pyplot as plt

def benchmark_linear_vs_quadratic():
    linear_times = []
    quadratic_times = []
    sizes = [1000, 2000, 4000, 8000, 16000]
    
    print(f"{'Size (N)':<10}{'O(N) Time (ms)':<18}{'O(N^2) Time (ms)'}")
    for n in sizes:
        # Algoritma O(N)
        t0 = time.perf_counter()
        _ = sum(range(n))
        t_lin = (time.perf_counter() - t0) * 1000
        linear_times.append(t_lin)
        
        # Algoritma O(N^2) (disimulasikan dengan nested pair check sederhana)
        t0 = time.perf_counter()
        _ = sum(i for i in range(min(n, 4000)) for _ in range(min(n, 4000)))
        t_quad = (time.perf_counter() - t0) * 1000
        quadratic_times.append(t_quad)
        
        print(f"{n:<10}{t_lin:<18.4f}{t_quad:.4f}")

benchmark_linear_vs_quadratic()
```""",
            "pitfalls": "Mengabaikan konstanta tersembunyi (*hidden constants*) dan efek cache CPU: algoritma $O(N \\log N)$ dengan overhead pointer dereference besar bisa berjalan jauh lebih lambat daripada algoritma $O(N^2)$ ramah-cache pada ukuran $N$ kecil ($N < 64$).",
            "exercises": "Level 1: Buktikan menggunakan definisi limit bahwa $3n^2 + 5n \\log n = O(n^2)$. Level 2: Selesaikan relasi rekurensi MergeSort $T(n) = 2T(n/2) + O(n)$ menggunakan Teorema Master. Level 3: Gunakan Metode Potensial (Potential Method) untuk membuktikan kompleksitas waktu teramortisasi operasi push dan pop pada Dynamic Array berfaktor ekspansi 1.5x.",
            "references": "- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms (4th ed.)*. MIT Press.\n- Sedgewick, R., & Wayne, K. (2011). *Algorithms (4th ed.)*. Addison-Wesley."
        },
        109: {
            "intuition": "Bagaimana teks kode bahasa Inggris yang Anda ketik di editor bisa berubah menjadi jutaan denyut listrik saklar transistor di silikon chip? Kompiler adalah penerjemah paling canggih di dunia: ia membedah kata per kata (Lexing), menyusunnya menjadi pohon tata bahasa logis (Parsing / AST), menyederhanakan logika matematika yang boros (Optimization SSA), lalu menerjemahkannya ke bahasa mesin biner yang langsung dimengerti CPU.",
            "theory": """
Tahapan Arsitektur Kompiler Modern (LLVM Pipeline):
1. **Frontend**: Kode Sumber $\\to$ Tokens (Lexer) $\\to$ Abstract Syntax Tree (Parser LL/LR/Pratt) $\\to$ Semantic Analysis & Type Checking.
2. **Intermediate Representation (IR)**: Transformasi ke bentuk **Static Single Assignment (SSA)** di mana setiap variabel hanya di-assign tepat satu kali, memfasilitasi optimasi aliran data via $\\phi$-functions.
3. **Optimizer (Middle-end)**:
   - Dead Code Elimination (DCE)
   - Constant Propagation & Folding
   - Common Subexpression Elimination (CSE)
   - Loop Vectorization & Inlining
4. **Backend**: Instruction Selection (ISel via Tree Rewriting) $\\to$ Register Allocation (Graph Coloring Chaitin-Briggs) $\\to$ Instruction Scheduling $\\to$ Machine Code Emission (ELF object file).
""",
            "internals": "Dalam bentuk SSA Form IR, analisis aliasing pointer dan dead-code elimination menjadi sangat efisien karena dependensi nilai (*use-def chains*) terjamin eksplisit dan unik secara global tanpa ambiguitas mutasi variabel runtime.",
            "code_block": """```python
import re

# Mini Arithmetic Lexer & Recursive Descent Parser ke AST
class ASTNode:
    def __init__(self, op, left=None, right=None, value=None):
        self.op = op
        self.left = left
        self.right = right
        self.value = value
    def __repr__(self):
        if self.value is not None: return str(self.value)
        return f"({self.left} {self.op} {self.right})"

def tokenize(expr):
    return re.findall(r'\\d+|[+\\-*/()]', expr)

class MiniParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token
    def parse_factor(self):
        token = self.consume()
        if token == '(':
            node = self.parse_expr()
            self.consume() # consume ')'
            return node
        return ASTNode(op='CONST', value=int(token))
    def parse_term(self):
        node = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume()
            node = ASTNode(op=op, left=node, right=self.parse_factor())
        return node
    def parse_expr(self):
        node = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            node = ASTNode(op=op, left=node, right=self.parse_term())
        return node

tokens = tokenize("3 + 4 * (2 - 1)")
parser = MiniParser(tokens)
ast = parser.parse_expr()
print("Hasil Parsing ke Abstract Syntax Tree (AST):", ast)
```""",
            "pitfalls": "Undefined Behavior (UB) di bahasa C/C++: kompiler modern mengasumsikan bahwa UB tidak akan pernah terjadi, sehingga optimasi SSA dapat menghapus seluruh pengecekan keamanan (security checks) yang Anda tulis jika pengecekan tersebut berada setelah operasi yang memicu signed integer overflow atau null pointer dereference.",
            "exercises": "Level 1: Tulis lexer Regex sederhana untuk membedah token angka, identifier, dan operator matematika. Level 2: Implementasikan Pratt Parser (Top-Down Operator Precedence) untuk mengevaluasi ekspresi dengan prioritas operator bervariasi. Level 3: Rancang kompilasi mini bahasa ekspresi langsung ke LLVM IR menggunakan library `llvmlite` di Python.",
            "references": "- Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools (Dragon Book)*. Pearson.\n- Cooper, K. D., & Torczon, L. (2011). *Engineering a Compiler*. Morgan Kaufmann."
        }
    }
    if topic_id in cs_catalog:
        return cs_catalog[topic_id]
    return _build_generic_systems(topic_id, slug, full_title, "Computer Science Core, Algoritma & Compiler")

def _gen_tier_7(topic_id, slug, full_title):
    os_catalog = {
        111: {
            "intuition": "Bayangkan sistem operasi seperti sebuah negara kerajaan. Aplikasi pengguna (browser, game) adalah rakyat biasa yang tinggal di luar istana (User Space / Ring 3). Mereka dilarang keras menyentuh langsung brankas emas atau senjata militer (hardware memori, disk, CPU control register). Jika rakyat ingin membaca data dari disk, mereka harus mengetuk pintu gerbang istana dan meminta izin kepada menteri kerajaan (Kernel Space / Ring 0) melalui jalur resmi yang diawasi ketat (System Call).",
            "theory": """
Model Hak Akses Cincin CPU (x86 Protection Rings):
- **Ring 0 (Kernel Mode)**: Hak akses tak terbatas ke seluruh instruksi CPU istimewa (misal: `lgdt`, `lidt`, `mov cr3, rax`, `cli`, `sti`, `wrmsr`) dan seluruh ruang alamat memori fisik.
- **Ring 3 (User Mode)**: Hak akses terbatas. Akses langsung ke hardware I/O (`in`, `out`) dan register kontrol memicu interupsi kesalahan proteksi umum (**General Protection Fault #GP**).

Mekanisme Transisi Ring:
Instruksi `syscall` (pada x86-64) atau `svc` (pada ARM64):
1. Hardware CPU secara otomatis menyimpan alamat instruksi berikutnya ($RIP$) ke register $RCX$, dan flags prosesor ke $R11$.
2. CPU beralih dari level privilese Ring 3 ke Ring 0.
3. CPU melompat ke alamat fungsi dispatch kernel yang telah didaftarkan sebelumnya di Model-Specific Register `MSR_LSTAR` ($0xC0000082$).
4. Kernel beralih dari User Stack pointer ke Kernel Stack pointer milik proses tersebut.
""",
            "internals": "vDSO (*virtual Dynamic Shared Object*) adalah mekanisme akselerasi kernel Linux di mana halaman memori kernel tertentu (seperti pembacaan jam sistem `clock_gettime`) dipetakan secara read-only ke ruang user space, memungkinkan syscall berkecepatan tinggi tanpa overhead pergantian konteks ring CPU (*zero context switch overhead*).",
            "code_block": """```c
#define _GNU_SOURCE
#include <unistd.h>
#include <sys/syscall.h>
#include <stdio.h>

int main(void) {
    char message[] = "Hello from direct Raw System Call!\\n";
    long written_bytes;
    
    // Pemanggilan langsung syscall write(1, message, sizeof(message)-1)
    // tanpa melalui wrapper standard library printf/puts
    __asm__ volatile (
        "mov $1, %%rax\\n"          // Syscall number untuk sys_write pada x86-64 = 1
        "mov $1, %%rdi\\n"          // Argumen 1: File descriptor stdout = 1
        "mov %1, %%rsi\\n"          // Argumen 2: Buffer pointer
        "mov %2, %%rdx\\n"          // Argumen 3: Jumlah byte
        "syscall\\n"                // Eksekusi transisi ke Ring 0 Kernel
        "mov %%rax, %0\\n"          // Tangkap return value
        : "=r" (written_bytes)
        : "r" (message), "r" ((long)(sizeof(message) - 1))
        : "rax", "rdi", "rsi", "rdx", "rcx", "r11", "memory"
    );
    
    printf("Syscall dieksekusi langsung! Jumlah byte tertulis: %ld\\n", written_bytes);
    return 0;
}
```""",
            "pitfalls": "Tergoda menulis system call di dalam inner-loop aplikasi berkinerja tinggi: setiap transisi syscall menelan biaya ratusan siklus CPU (akibat flush pipeline, pemeriksaan permission, dan pengamanan spekulatif mitigasi Meltdown/Spectre KPTI). Solusi modern: gunakan antarmuka asinkron batching seperti `io_uring`.",
            "exercises": "Level 1: Gunakan utility `strace` di terminal Linux untuk merekam dan menghitung semua system call yang dieksekusi oleh perintah `ls -l`. Level 2: Buat program C yang mengimplementasikan syscall custom wrapper menggunakan fungsi `syscall(SYS_getpid)`. Level 3: Tulis modul kernel Linux sederhana (LKM) yang mendaftarkan karakter device dan membaca memory buffer dari user-space menggunakan `copy_from_user`.",
            "references": "- Bovet, D. P., & Cesati, M. (2005). *Understanding the Linux Kernel*. O'Reilly Media.\n- Love, R. (2010). *Linux Kernel Development (3rd ed.)*. Addison-Wesley."
        },
        120: {
            "intuition": "Bayangkan Anda memesan pizza dari 100 restoran berbeda. Pendekatan lama (blocking I/O) seperti menelepon restoran pertama, menunggu 30 menit di telepon sampai pizza tiba di pintu, baru kemudian menelepon restoran kedua. Pendekatan asinkron modern (epoll / io_uring) seperti menitipkan daftar pesanan ke satu kurir pintar: kurir pergi mengurus semuanya di latar belakang, dan Anda cukup memeriksa papan notifikasi di meja saat ada paket pizza yang siap dimakan!",
            "theory": """
Evolusi Mekanisme I/O Multiplexing Linux:
1. **select() / poll()**: Kompleksitas $O(N)$ di mana kernel harus memindai seluruh array file descriptor setiap kali dipanggil.
2. **epoll()**: Kompleksitas $O(1)$ berbasis event callback kernel menggunakan struktur data Red-Black Tree untuk tracking FD dan Wait Queue berbasis ready-list.
   - Mode *Level-Triggered (LT)*: Memberi tahu berulang kali selama buffer masih ada data.
   - Mode *Edge-Triggered (ET)*: Hanya memberi tahu satu kali saat transisi status buffer terjadi (membutuhkan loop non-blocking read hingga `EAGAIN`).
3. **io_uring (Linux 5.1+)**:
   Arsitektur antarmuka I/O berbasis dua Ring Buffer murni di memori bersama (*shared memory*) antara kernel dan user-space:
   - **Submission Queue (SQ)**: User space mengisi request I/O tanpa system call.
   - **Completion Queue (CQ)**: Kernel mengisi hasil I/O yang telah rampung secara asinkron.
   - Meniadakan overhead system call sepenuhnya menggunakan fitur kernel thread polling (`IORING_SETUP_SQPOLL`).
""",
            "internals": "Dengan `io_uring`, jutaan operasi baca/tulis disk NVMe dan jaringan dapat diproses per detik per core karena tidak ada lagi interupsi software dan pergantian konteks kernel-space/user-space untuk setiap transaksi IO tunggal.",
            "code_block": """```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/epoll.h>
#include <unistd.h>
#include <fcntl.h>

#define MAX_EVENTS 10

void set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main(void) {
    // 1. Buat instance epoll
    int epfd = epoll_create1(0);
    if (epfd < 0) { perror("epoll_create1"); return 1; }
    
    // Pantau standard input (stdin / fd 0)
    set_nonblocking(0);
    struct epoll_event ev, events[MAX_EVENTS];
    ev.events = EPOLLIN | EPOLLET; // Edge-Triggered
    ev.data.fd = 0;
    
    if (epoll_ctl(epfd, EPOLL_CTL_ADD, 0, &ev) < 0) {
        perror("epoll_ctl"); return 1;
    }
    
    printf("Menunggu input pada stdin via non-blocking epoll (Ketik sesuatu dan tekan Enter)...\\n");
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, 5000); // 5 detik timeout
    
    if (nfds == 0) {
        printf("Timeout 5 detik berakhir, tidak ada input.\\n");
    } else {
        char buf[256];
        int n = read(events[0].data.fd, buf, sizeof(buf)-1);
        if (n > 0) {
            buf[n] = '\\0';
            printf("Event terbaca (%d bytes): %s", n, buf);
        }
    }
    close(epfd);
    return 0;
}
```""",
            "pitfalls": "Pada epoll Edge-Triggered (ET), jika Anda membaca data kurang dari total data di buffer soket dan keluar dari loop tanpa membaca `EAGAIN`, soket akan terhenti (*starvation*) selamanya karena epoll ET tidak akan pernah membangkitkan notifikasi baru untuk sisa data lama.",
            "exercises": "Level 1: Jelaskan perbedaan matematis dan skalabilitas memori antara `select()` dengan limit 1024 FD vs `epoll()`. Level 2: Bangun TCP Echo Server berkinerja tinggi menggunakan C dan `epoll` non-blocking yang mampu menangani 10.000 koneksi simultan (C10K problem). Level 3: Implementasikan pembacaan file asinkron multithreaded menggunakan antarmuka Linux `io_uring` murni via liburing.",
            "references": "- Kerrisk, M. (2010). *The Linux Programming Interface*. No Starch Press.\n- Axboe, J. (2019). *Efficient IO with io_uring*. Kernel Documentation."
        }
    }
    if topic_id in os_catalog:
        return os_catalog[topic_id]
    return _build_generic_systems(topic_id, slug, full_title, "Operating Systems Internals & Linux")

def _build_generic_systems(topic_id, slug, full_title, tier_category):
    return {
        "intuition": f"Dalam rekayasa sistem komputer tingkat rendah, konsep **{full_title}** adalah pondasi arsitektural yang mengatur bagaimana instruksi, sinyal, proses, atau memori berinteraksi secara deterministik dan berkecepatan tinggi tanpa kegagalan.",
        "theory": (
            f"Model formal dan parameter sistem untuk {full_title}:\n"
            r"$$\Delta T_{latency} = \sum_{k=1}^M \tau_{propagation} + \frac{\text{Payload}}{\text{Bandwidth}} + T_{arbitration}$$" + "\n"
            "Di mana status mesin dijamin konsisten melalui protokol sinkronisasi hardware/kernel dengan kepatuhan terhadap invariants keselamatan (*safety invariants*) dan kebebasan dari deadlock (*liveness properties*).\n"
        ),
        "internals": f"""
```mermaid
sequenceDiagram
    participant User as Aplikasi / Thread
    participant Kernel as Core / Dispatcher
    participant HW as Hardware Controller
    User->>Kernel: Request Transaksi ({slug})
    Kernel->>HW: Direct Memory Access / Register Write
    HW-->>Kernel: Hardware Interrupt / Signal Complete
    Kernel-->>User: Return Status (Zero Error)
```
Mekanisme eksekusi melibatkan alokasi register cepat, penanganan tabel descriptor memori, dan penyelarasan cache-line untuk mencegah *false sharing*.
""",
        "code_block": f"""```c
// Implementasi Standar Sistem: {slug}
#include <stdio.h>
#include <stdint.h>

typedef struct {{
    uint32_t status_flags;
    uint64_t memory_address;
    uint32_t buffer_length;
}} SystemDescriptor_t;

int main(void) {{
    SystemDescriptor_t desc = {{
        .status_flags = 0x01,
        .memory_address = 0x7FFF0000,
        .buffer_length = 4096
    }};
    printf("Modul %03d: Inisialisasi sistem %s berhasil dieksekusi.\\n", {topic_id}, "{slug}");
    return 0;
}}
```""",
        "pitfalls": f"Jebakan fatal pada {full_title} adalah race condition antara interupsi hardware dan eksekusi software, kegagalan penyelarasan memori (*unaligned memory access*), atau kebocoran resource handle.",
        "exercises": f"""
### Level 1 (Dasar)
Gambarkan diagram alur bagaimana kontrol berpindah dari software ke hardware saat konsep {full_title} dijalankan.

### Level 2 (Menengah)
Bangun implementasi kode bersih dalam C/Rust/Assembly yang menguji ketahanan sistem terhadap kondisi batas atau konkurensi tinggi.

### Level 3 (Mahir)
Lakukan profiling performa mendalam menggunakan tools seperti `perf`, osiloskop, atau logic analyzer untuk mengidentifikasi bottleneck latensi nanodetik.
""",
        "references": f"- Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts*. Wiley.\n- Hennessy, J. L., & Patterson, D. A. (2017). *Computer Architecture: A Quantitative Approach*. Morgan Kaufmann."
    }
