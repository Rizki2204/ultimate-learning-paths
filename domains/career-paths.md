# Microelectronics

Microelectronics is the study and design of electronic circuits at the transistor and IC (integrated circuit) level: semiconductor physics, device modeling, analog/digital circuits, layout, and fabrication basics.

## Core learning goals
- Understand semiconductor physics and MOS transistor operation
- Learn analog circuit fundamentals (op-amps, filters)
- Learn digital CMOS design principles
- Understand IC layout and parasitics
- Learn testing, verification, and fabrication basics

## Learning sequence

### A. Foundations (0-3 months)
- Basic electronics: resistors, capacitors, inductors, Ohm's law
- Basic circuit analysis (Kirchhoff laws)
- Semiconductor basics: diodes, BJT

### B. MOSFET & CMOS basics (3-6 months)
- MOS transistor operation (Vgs, Vth, Ids)
- CMOS logic gates and static CMOS design
- Noise margins, sizing, and ratioed logic
- Basic analog transistor circuits

### C. Analog circuits and mixed-signal (6-12 months)
- Operational amplifier fundamentals
- Filters and signal conditioning
- ADC/DAC basics and interface
- PLLs and clocking basics
- Mixed-signal considerations and clock domain crossing

### D. IC layout & fabrication (9-18 months)
- Layout rules and design rule checking (DRC)
- Parasitic capacitance and resistance
- Process steps: diffusion, oxidation, lithography, etching, doping, metallization
- LVS (layout vs schematic) and verification

### E. Advanced topics (18+ months)
- Low-power design techniques
- Analog/RF design basics
- MEMS basics (optional)
- EDA toolflows and scripting
- Design for testability (DFT) and scan

## Tools & repos
- KiCad (PCB, not IC): https://github.com/KiCad
- OpenROAD project (VLSI flow): https://github.com/The-OpenROAD-Project
- Qflow and other open-source EDA tools
- Textbooks: Sedra/Smith, Razavi, Gray & Meyer for analog

## Projects ladder
- Beginner: build and simulate op-amp circuits in SPICE
- Intermediate: design CMOS logic at transistor level and simulate
- Advanced: use OpenROAD flow to synthesize and place-and-route a small digital block

## Suggested reading
- "Microelectronic Circuits" by Sedra & Smith
- "CMOS VLSI Design" by Weste & Harris
- "Design of Analog CMOS Integrated Circuits" by Behzad Razavi

## Checkpoints
- [ ] Can analyze transistor-level circuits
- [ ] Understand CMOS logic implementation
- [ ] Can simulate analog circuits in SPICE
- [ ] Familiar with IC flow concepts (synthesis, P&R, DRC/LVS)

## Related domains
- Computer Engineering
- Embedded Systems
- PCB design and manufacturing
