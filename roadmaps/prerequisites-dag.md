# Prerequisites Directed Acyclic Graph (DAG) — Peta Ketergantungan Topik

Dokumen ini memetakan hubungan logis dan prasyarat antar-tingkat pembelajaran dalam kurikulum **17 Tingkat (Tingkat 0 s/d 16)**. Struktur kurikulum dirancang sebagai **Directed Acyclic Graph (DAG)** di mana Anda dapat mempelajari topik-topik secara linear atau melintasi jalur spesialisasi peran (*role-based learning tracks*).

---

## 🗺️ Diagram Ketergantungan Tingkat Utama

```mermaid
flowchart TD
    T0["Tingkat 0: Fondasi Kognitif & Logika (1-5)"] --> T1["Tingkat 1: Matematika Komprehensif (6-23)"]
    T0 --> T2["Tingkat 2: Fisika & Semikonduktor (24-37)"]
    
    T1 --> T6["Tingkat 6: CS Core, DSA & Compilers (88-109)"]
    T1 --> T8["Tingkat 8: DSP & Jaringan Komputer (125-139)"]
    T1 --> T12["Tingkat 12: Data Science & AI/MLOps (183-195)"]
    T1 --> T14["Tingkat 14: Fintech, HFT & Blockchain (207-216)"]
    
    T2 --> T3["Tingkat 3: Rangkaian & Mikroelektronika (38-52)"]
    T3 --> T4["Tingkat 4: Logika Digital & CPU Architecture (53-69)"]
    
    T4 --> T5["Tingkat 5: Embedded Systems & RTOS (70-87)"]
    T4 --> T7["Tingkat 7: Linux & OS Internals (110-124)"]
    
    T6 --> T7
    T6 --> T9["Tingkat 9: Software Engineering & Cloud SRE (140-156)"]
    T6 --> T10["Tingkat 10: Basis Data & Enterprise (157-167)"]
    T6 --> T11["Tingkat 11: Cyber Security & Reverse Eng (168-182)"]
    
    T7 --> T11
    T8 --> T9
    T9 --> T10
    
    T12 --> T13["Tingkat 13: Sains Kognitif & NLP (196-206)"]
    T5 --> T15["Tingkat 15: Robotika, Mekatronika & Kendali (217-226)"]
    T12 --> T15
    
    T6 --> T16["Tingkat 16: HPC, Multimedia & Quantum (227-232)"]
    T1 --> T16
    T4 --> T16
```

---

## 🎯 Jalur Spesialisasi Karier & Rekayasa

### 1. Jalur AI Systems & LLM Architect
- **Urutan Belajar**: Tingkat 0 $\to$ Tingkat 1 (Aljabar Linier, Probabilitas, Optimasi) $\to$ Tingkat 6 (Struktur Data) $\to$ Tingkat 12 (Machine Learning, Autograd, CUDA) $\to$ Tingkat 13 (Transformer, MoE, RLHF, Autonomous Agents).
- **Fokus Utama**: Matematika tensor, pemrograman CUDA GPU, arsitektur attention, scaling laws, dan MLOps.

### 2. Jalur Embedded Systems, Firmware & Robotics Engineer
- **Urutan Belajar**: Tingkat 0 $\to$ Tingkat 2 (Fisika, Semikonduktor) $\to$ Tingkat 3 (Rangkaian Listrik, MOSFET) $\to$ Tingkat 4 (Digital Logic, CPU) $\to$ Tingkat 5 (Bare-Metal C, DMA, RTOS) $\to$ Tingkat 15 (Kinematika DH, PID/LQR, ROS 2, SLAM).
- **Fokus Utama**: Manipulasi bitwise, interupsi NVIC, osiloskop, kendali motor FOC, dan simulator Gazebo.

### 3. Jalur Low-Level Systems, Kernel & Security Researcher
- **Urutan Belajar**: Tingkat 0 $\to$ Tingkat 1 (Matematika Diskrit) $\to$ Tingkat 4 (Arsitektur Komputer x86-64/ARM) $\to$ Tingkat 6 (Compilers, C, Memory Management) $\to$ Tingkat 7 (Linux OS Internals, Syscalls, eBPF) $\to$ Tingkat 11 (Kriptografi, Binary Exploitation ROP, Kernel Pwn).
- **Fokus Utama**: Disassembling Ghidra, bypass mitigasi memori, reverse engineering, dan audit kernel Linux.

### 4. Jalur Quantitative Trading, Financial Engineering & HFT
- **Urutan Belajar**: Tingkat 0 $\to$ Tingkat 1 (Kalkulus Stokastik, Time Series, Game Theory) $\to$ Tingkat 4 (Arsitektur CPU Cache, Bus PCIe) $\to$ Tingkat 6 (DSA Berkinerja Tinggi) $\to$ Tingkat 14 (Mikrostruktur Pasar LOB, Lock-Free SPSC C++, Kernel-Bypass DPDK, FPGA).
- **Fokus Utama**: Zero-allocation C++, protokol NASDAQ ITCH, persamaan Black-Scholes, dan latensi sub-mikrodetik.

---
*Kembali ke: [Master Index](../INDEX.md) | [Portal Utama](../README.md)*