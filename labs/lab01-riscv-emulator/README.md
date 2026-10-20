# Laboratory 01: RV32I RISC-V CPU Emulator

## 1. Architectural Overview
This laboratory implements a Cycle-Accurate 32-bit RISC-V (RV32I) Central Processing Unit emulator in ANSI C (C99/C11). The emulator executes uncompressed 32-bit RISC-V machine instructions conforming strictly to the RISC-V Unprivileged and Privileged Architecture Specifications.

```
+-------------------------------------------------------------------+
|                        RV32I CPU Core                             |
|                                                                   |
|   +-----------------------+     +-----------------------------+   |
|   | General Registers     |     | Control & Status Registers  |   |
|   | x0 (Hardwired Zero)   |     | mstatus (0x300)             |   |
|   | x1 (Return Address)   |     | mtvec   (0x305)             |   |
|   | x2 (Stack Pointer)    |     | mepc    (0x341)             |   |
|   | x3..x31 (General Regs)|     | mcause  (0x342)             |   |
|   +-----------------------+     +-----------------------------+   |
|               ^                               ^                   |
|               |                               |                   |
|   +-----------------------+     +-----------------------------+   |
|   | Arithmetic Logic Unit |<--->| Instruction Decoder         |   |
|   | ADD, SUB, SLT, SLTU,  |     | R-Type, I-Type, S-Type,     |   |
|   | SLL, SRL, SRA, XOR/OR |     | B-Type, U-Type, J-Type      |   |
|   +-----------------------+     +-----------------------------+   |
|               |                               ^                   |
+---------------|-------------------------------|-------------------+
                v                               |
    +-------------------------------------------------------+
    |                     System Bus                        |
    +-------------------------------------------------------+
                |                               |
                v                               v
    +-----------------------+       +-----------------------+
    | Main Memory (RAM)     |       | Memory Mapped I/O     |
    | Base: 0x80000000      |       | Base: 0x10000000      |
    | Size: 16 Megabytes    |       | UART TX Console Out   |
    +-----------------------+       +-----------------------+
```

## 2. Memory Map & Register Architecture
The simulated system maps physical addresses as follows:

| Region | Start Address | End Address | Purpose |
|---|---|---|---|
| **UART MMIO** | `0x10000000` | `0x10000FFF` | Console output transmit register. Writing a byte writes directly to standard out or emulator buffer. |
| **System RAM** | `0x80000000` | `0x80FFFFFF` | 16 MB Little-Endian Physical RAM containing instructions, stack, and heap. |

### Register Conventions
- `x0`: Hardwired zero. Any write to `x0` is discarded; reads always return `0x00000000`.
- `x1`: Return address (`ra`).
- `x2`: Stack pointer (`sp`).
- `pc`: Program counter initialized to `0x80000000`.

## 3. Instruction Set Support Matrix
The emulator fully implements the RV32I base instruction set:
- **Integer Register-Register Operations (R-Type)**: `ADD`, `SUB`, `SLL`, `SLT`, `SLTU`, `XOR`, `SRL`, `SRA`, `OR`, `AND`.
- **Integer Register-Immediate Operations (I-Type)**: `ADDI`, `SLTI`, `SLTIU`, `XORI`, `ORI`, `ANDI`, `SLLI`, `SRLI`, `SRAI`.
- **Load and Store Operations (I/S-Type)**: `LB`, `LH`, `LW`, `LBU`, `LHU`, `SB`, `SH`, `SW`.
- **Control Transfer (B/J-Type)**: `BEQ`, `BNE`, `BLT`, `BGE`, `BLTU`, `BGEU`, `JAL`, `JALR`.
- **Upper Immediate Operations (U-Type)**: `LUI`, `AUIPC`.
- **Privileged and System Operations**: `ECALL`, `EBREAK`, `CSRRW`, `CSRRS`, `CSRRC`, `MRET`.

## 4. Scaffolding & Directory Structure
```
labs/lab01-riscv-emulator/
├── README.md               # Architecture documentation
├── Makefile                # Root build and test automation
├── run_tests.py            # Standalone unittest runner (exit code 0)
├── include/                # Header definitions
│   ├── riscv.h             # Architectural constants and opcodes
│   ├── mmu.h               # Memory Management Unit API
│   ├── instructions.h      # Instruction decode and execution structs
│   └── cpu.h               # CPU state and step execution API
├── starter/                # Student starter scaffolding
│   ├── Makefile            # Starter compilation rules
│   └── cpu_starter.c       # Clean skeleton with contract definitions
├── src/                    # Complete production reference implementation
│   ├── mmu.c               # RAM and MMIO UART handling
│   ├── instructions.c      # RV32I instruction decode and ALU dispatch
│   ├── cpu.c               # State transitions, registers, and fetch cycle
│   └── main.c              # CLI interface and self-test harness
└── tests/                  # Automated test suite
    ├── riscv_helpers.py    # Binary instruction pack utilities
    ├── test_alu.py         # ALU and bitwise logic test vectors
    ├── test_memory.py      # Store/load word, halfword, byte, and UART
    ├── test_branch.py      # Branch conditionals, JAL, and JALR
    └── test_programs.py    # Full algorithms: Fibonacci, GCD, string reverse
```

## 5. Milestone Progression Guide
1. **Milestone 1 (Registers & Memory Bus)**:
   Implement `mmu_read32` and `mmu_write32` with little-endian byte ordering. Enforce `x0 == 0` invariant on register writes.
2. **Milestone 2 (Immediate Field Decoding)**:
   Extract signed immediate values with two's complement sign extension for I, S, B, U, and J instruction formats.
3. **Milestone 3 (ALU Register-Immediate & Register-Register)**:
   Implement arithmetic, bitwise, shift, and set-less-than instructions.
4. **Milestone 4 (Memory Access & MMIO)**:
   Implement `LB`, `LBU`, `LH`, `LHU`, `LW`, `SB`, `SH`, `SW`. Connect `0x10000000` to the UART output console buffer.
5. **Milestone 5 (Branches & Jumps)**:
   Implement PC-relative branching with signed comparisons, unconditional jump-and-link (`JAL`), and indirect jump-and-link (`JALR`).
6. **Milestone 6 (Traps & Verification)**:
   Add `ECALL` and `CSR` handling. Execute the automated test suite to confirm end-to-end algorithmic correctness.

## 6. Verification and Execution
Run the complete automated test suite:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
The test suite compiles the C binary natively and validates 17 comprehensive unit and integration test vectors within 200 milliseconds.
