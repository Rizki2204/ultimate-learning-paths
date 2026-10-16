# Computer Engineering

Computer Engineering bridges hardware and software: processor design, digital logic, computer architecture, embedded systems, and interfacing hardware with software.

## Core learning goals
- Understand digital logic and circuit theory
- Learn CPU architecture and microarchitecture
- Learn memory systems and cache behavior
- Master interfacing (buses, I/O) and embedded-software co-design
- Learn RTL (Verilog/VHDL), simulation, FPGA flows
- Understand SoC design and basic EDA flows

## Detailed learning sequence (from 0 → professional)

### A. Foundations (0-3 months)
- Basic electricity and circuits: voltage, current, resistance, Ohm's law
- Binary/hexadecimal, boolean algebra
- Basic logic gates and truth tables
- Combinational and sequential circuits
- Simple circuits on breadboard

### B. Digital Design & Logic (3-6 months)
- Karnaugh maps, minimization
- Multiplexer, demultiplexer, encoder, decoder
- Adders, subtractors, ALU basics
- Registers, counters, shift registers
- Finite State Machines (Moore/Mealy)
- Timing: setup/hold, propagation delay

### C. Computer Architecture (6-12 months)
- Von Neumann vs Harvard architectures
- Instruction set architecture (ISA) basics
- CPU datapath and control
- Pipelining and hazards
- Superscalar, out-of-order concepts (intro)
- Memory hierarchy: caches, TLB
- I/O and DMA
- Interrupts and exception handling

### D. RTL, FPGA, and SoC (9-18 months)
- Verilog or VHDL basics
- Simulation with ModelSim/iverilog
- Synthesis basics and constraints
- FPGA fabric: LUTs, CLBs, BRAM, DSP slices
- Toolchains: Yosys, nextpnr, SymbiFlow
- Softcore processors (e.g., RISC-V implementations)
- SoC integration basics

### E. Embedded-Software Co-design (12-24 months)
- Bare-metal firmware programming
- Low-level device drivers
- Interrupt-driven programming
- Bootloaders and startup sequences
- Performance analysis and power optimization

### F. Advanced topics / Specialization (18+ months)
- ASIC design flows (front-end/back-end) — optional for industry
- High-performance microarchitectures
- Advanced memory systems
- Formal verification basics
- Hardware security (side-channel, secure boot)

## Practical tools & repos
- lowRISC/ibex (RISC-V core): https://github.com/lowRISC/ibex
- litex-hub/litex and cores: https://github.com/litex-hub
- SymbiFlow ecosystem: https://github.com/SymbiFlow
- yosysHQ/yosys: https://github.com/YosysHQ/yosys
- FPGA tools and examples: https://github.com/SymbiFlow/prjtrellis
- risc-v/riscv-isa-manual: https://github.com/riscv/riscv-isa-manual

## Projects ladder
- Beginner: build simple combinational circuits on breadboard (binary adder, multiplexer)
- Intermediate: design FSM in Verilog and simulate; implement simple CPU datapath
- Advanced: build a RISC-V softcore on FPGA and run a small RTOS
- Professional: design and verify a custom SoC subsystem and integrate peripherals

## Recommended textbooks & courses
- "Digital Design and Computer Architecture" by Harris & Harris
- "Computer Organization and Design" by Patterson & Hennessy
- "Digital Design" by M. Morris Mano
- Coursera / edX courses: Computer Architecture, Digital Systems

## Checkpoints
- [ ] Can design combinational and sequential circuits
- [ ] Understand pipelining and hazards
- [ ] Can write Verilog for basic modules and simulate them
- [ ] Have experience with at least one FPGA workflow
- [ ] Implemented a small CPU or peripheral

## Next domains to pair with
- Embedded Systems
- Microelectronics
- Software Engineering
