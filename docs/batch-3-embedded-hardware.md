# Batch 3 deep dive: Embedded systems, computer engineering, and microelectronics

This batch covers the hardware/software boundary: firmware, microcontrollers, digital logic, CPU architecture, and the systems that control real devices.

## Why this matters

Embedded and hardware engineering connect:
- software and hardware interaction
- firmware and device drivers
- circuits and real-time constraints
- sensors and peripherals
- power, reliability, and physical signals

This field is essential for robotics, industrial automation, IoT, automotive, electronics, and many advanced engineering roles.

---

## Learning flow

### Phase A: Electronics fundamentals (Weeks 1-6)

#### Topics
- voltage, current, resistance
- Ohm's law
- circuit basics
- breadboards and prototyping
- resistors, capacitors, inductors
- diodes, transistors, MOSFETs
- power and grounding
- reading schematics
- basic measurement tools

#### Tools
- multimeter
- breadboard
- basic oscilloscope (or beginner hardware kit)
- logic analyzer optional

#### Projects
- LED circuits
- push button logic
- PWM brightness control
- sensor reading circuit

#### Milestones
- [ ] Understand basic circuit behavior
- [ ] Read a simple schematic
- [ ] Build a working prototype on breadboard

---

### Phase B: Digital logic and computer architecture (Weeks 6-14)

#### Topics
- Boolean algebra
- logic gates
- combinational logic
- sequential logic
- registers and counters
- finite state machines
- CPU basics
- datapath and control paths
- memory hierarchy
- caches and virtual memory basics
- pipelining basics
- interrupts and exceptions

#### Tools
- logic simulation tools
- Verilog or VHDL basics
- FPGA tools and examples

#### Good repositories
- lowRISC/ibex: https://github.com/lowRISC/ibex
- litex-hub/litex: https://github.com/litex-hub/litex
- yosysHQ/yosys: https://github.com/YosysHQ/yosys
- SymbiFlow: https://github.com/SymbiFlow
- riscv/riscv-isa-manual: https://github.com/riscv/riscv-isa-manual

#### Projects
- 4-bit adder in Verilog
- FSM design simulation
- simple register bank design
- basic CPU datapath concept

#### Milestones
- [ ] Design basic digital systems
- [ ] Write Verilog / HDL logic
- [ ] Understand CPU + memory interaction

---

### Phase C: Microcontrollers and firmware (Weeks 10-20)

#### Topics
- C for embedded systems
- pointers and memory layout
- interrupts and timers
- GPIO
- UART / SPI / I2C
- ADC / DAC / PWM
- watchdogs
- serial debugging
- sensor interfacing
- real-time constraints

#### Platforms
- Arduino
- ESP32
- STM32
- AVR/PIC boards
- Teensy (optional)

#### Tools
- PlatformIO
- Arduino IDE
- STM32CubeIDE
- ESP-IDF
- OpenOCD

#### Good repositories
- espressif/esp-idf: https://github.com/espressif/esp-idf
- micropython/micropython: https://github.com/micropython/micropython
- zephyrproject-rtos/zephyr: https://github.com/zephyrproject-rtos/zephyr
- FreeRTOS: https://github.com/FreeRTOS/FreeRTOS-Kernel

#### Projects
- temperature sensor logger
- smart lamp controller
- motor driver controller
- UART sensor gateway
- BLE or Wi-Fi sensor node

#### Milestones
- [ ] Program GPIO and timing logic
- [ ] Interface sensors and peripherals
- [ ] Understand interrupts and timers
- [ ] Debug firmware with serial logging

---

### Phase D: RTOS and real-time systems (Weeks 16-24)

#### Topics
- tasks and scheduling
- mutexes and semaphores
- interrupt-driven design
- real-time constraints
- memory planning
- power-aware design
- boot processes
- device drivers basics

#### Tools
- FreeRTOS
- Zephyr
- RTOS examples

#### Projects
- sensor fusion node
- motor and controller task scheduler
- communication gateway with tasks
- OTA update concept

#### Milestones
- [ ] Understand task scheduling and synchronization
- [ ] Design interrupt-driven firmware
- [ ] Build a small RTOS project

---

### Phase E: Microelectronics and IC concepts (Weeks 18-30)

#### Topics
- semiconductor physics basics
- diode and transistor behavior
- MOSFET operation
- CMOS logic fundamentals
- op-amp basics
- analog filter design
- IC fabrication flow
- parasitics and layout awareness
- DRC/LVS concepts

#### Tools
- KiCad
- SPICE-like simulators
- OpenROAD / EDA ecosystem basics

#### References
- "Microelectronic Circuits" by Sedra & Smith
- "CMOS VLSI Design" by Weste & Harris
- "Design of Analog CMOS Integrated Circuits" by Razavi

#### Project ideas
- analog amplifier simulation
- transistor-level logic design
- CMOS gate design experiment
- simple PCB prototype

#### Milestones
- [ ] Understand transistor-level behavior
- [ ] Understand CMOS and analog basics
- [ ] Understand IC design and layout flow

---

## Strong portfolio path

### Beginner projects
- LED blink system with user input
- button-controlled output
- sensor data logger

### Intermediate projects
- ESP32 sensor node with Wi-Fi
- UART/SPI/I2C device integration
- motor control with PID

### Advanced projects
- custom firmware with RTOS
- board bring-up and peripheral integration
- custom PCB with MCU and sensors
- embedded Linux / hardware + software integration project

---

## Best stack choices

### Embedded-focused path
- C, GPIO, UART, SPI, I2C, timers, interrupts, RTOS

### Hardware-focused path
- digital logic, Verilog, FPGA, device physics, CMOS, PCB design

### Mixed path
- C + electronics + sensors + RTOS + PCB + debug tools

---

## Final checklist

- [ ] Understand circuit fundamentals
- [ ] Can build prototypes on breadboard
- [ ] Understand digital logic
- [ ] Can write firmware in C
- [ ] Use serial debugging and peripherals
- [ ] Use interrupts and timers correctly
- [ ] Understand RTOS basics
- [ ] Can design a basic embedded system project

This domain is the bridge between software thinking and physical realities.

---

## Next domain in order

After embedded and hardware, the best next path is:
- AI / ML / Data Science
- then Cybersecurity / Networking
- then Robotics / Mechatronics / Automation
- then Cloud / DevOps / Data Engineering
