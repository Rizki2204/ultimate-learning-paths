# scripts/generate_all_topics.py
"""
Master generator script: Generates all 232 curriculum modules across 17 tiers,
along with tier READMEs, master INDEX.md, and roadmaps/prerequisites-dag.md.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from scripts.tier_definitions import TIERS, TOPICS_METADATA
from scripts.topic_knowledge_base import get_topic_payload
from scripts.encyclopedia.enricher_engine import enrich_topic_payload


def generate_tier_readmes():
    print("Generating 17 Tier READMEs...")
    for tier in TIERS:
        tier_idx = tier["index"]
        tier_dir = os.path.join(BASE_DIR, "curriculum", tier["dir_name"])
        os.makedirs(tier_dir, exist_ok=True)
        
        start_id, end_id = tier["topics_range"]
        tier_topics = [t for t in TOPICS_METADATA if start_id <= t[0] <= end_id]
        
        lines = [
            f"# {tier['title']}",
            "",
            f"**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Portal Utama](../../README.md)",
            "",
            "## 📌 Gambaran Umum & Misi Pembelajaran",
            tier["description"],
            "",
            "## 🎯 Sasaran Kompetensi",
            f"- Memahami konsep dasar dari nol mutlak hingga level profesional tanpa ada lompatan logika.",
            f"- Mampu mengimplementasikan simulasi kode riil dan memahami mekanisme internal hardware/software.",
            f"- Menyelesaikan proyek mandiri berjenjang di setiap modul materi.",
            "",
            f"## 📚 Daftar Modul Materi ({start_id:03d} - {end_id:03d})",
            "",
            "| No | Modul | Slug File | Status |",
            "|---|---|---|:---:|"
        ]
        
        for t_id, slug, full_title, _ in tier_topics:
            filename = f"{t_id:03d}-{slug}.md"
            lines.append(f"| {t_id:03d} | [{full_title}](./{filename}) | `{filename}` | ✅ Siap Pelajari |")
            
        lines.extend([
            "",
            "---",
            "*Gunakan modul ini secara berurutan atau ikuti panduan jalur spesialisasi di [Prerequisites DAG](../../roadmaps/prerequisites-dag.md).*"
        ])
        
        readme_path = os.path.join(tier_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
    print("All 17 Tier READMEs successfully created!")

def generate_topic_files():
    print("Generating all 232 Topic Modules (7-Layer In-Depth)...")
    total = len(TOPICS_METADATA)
    
    for idx, (t_id, slug, full_title, tier_idx) in enumerate(TOPICS_METADATA):
        tier = TIERS[tier_idx]
        tier_dir = os.path.join(BASE_DIR, "curriculum", tier["dir_name"])
        os.makedirs(tier_dir, exist_ok=True)
        
        raw_payload = get_topic_payload(t_id, slug, full_title, tier_idx)
        payload = enrich_topic_payload(t_id, slug, full_title, tier_idx, raw_payload)
        
        # Navigation links
        prev_meta = TOPICS_METADATA[idx - 1] if idx > 0 else None
        next_meta = TOPICS_METADATA[idx + 1] if idx < total - 1 else None
        
        if prev_meta:
            prev_tier = TIERS[prev_meta[3]]
            if prev_meta[3] == tier_idx:
                prev_link = f"[{prev_meta[0]:03d}. {prev_meta[1]}](./{prev_meta[0]:03d}-{prev_meta[1]}.md)"
            else:
                prev_link = f"[{prev_meta[0]:03d}. {prev_meta[1]}](../{prev_tier['dir_name']}/{prev_meta[0]:03d}-{prev_meta[1]}.md)"
        else:
            prev_link = "*Awal Kurikulum*"
            
        if next_meta:
            next_tier = TIERS[next_meta[3]]
            if next_meta[3] == tier_idx:
                next_link = f"[{next_meta[0]:03d}. {next_meta[1]}](./{next_meta[0]:03d}-{next_meta[1]}.md)"
            else:
                next_link = f"[{next_meta[0]:03d}. {next_meta[1]}](../{next_tier['dir_name']}/{next_meta[0]:03d}-{next_meta[1]}.md)"
        else:
            next_link = "*Puncak Kurikulum (Tuntas 100%)*"
            
        filename = f"{t_id:03d}-{slug}.md"
        filepath = os.path.join(tier_dir, filename)
        
        content = f"""# Modul {t_id:03d}: {full_title}

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat {tier_idx}: {tier['title']}](./README.md)
*Sebelumnya*: {prev_link} | *Berikutnya*: {next_link}

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
{payload['intuition'].strip()}

## 2. Fondasi Teoretis & Aksiomatik / Matematis
{payload['theory'].strip()}

## 3. Anatomi Teknis & Cara Kerja Internal
{payload['internals'].strip()}

## 4. Implementasi Praktis & Kode / Simulasi Riil
{payload['code_block'].strip()}

## 5. Miskonsepsi & Jebakan Industri
{payload['pitfalls'].strip()}

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
{payload['exercises'].strip()}

## 7. Rekomendasi Sumber Belajar Standar Emas
{payload['references'].strip()}

---
*Navigasi Cepat*: [Ke Tingkat {tier_idx}](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: {prev_link} | *Berikutnya*: {next_link}
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        if t_id % 25 == 0 or t_id == total:
            print(f" - Progress: {t_id}/{total} modules generated ({slug})...")
            
    print("All 232 Topic Modules successfully created!")

def generate_master_index():
    print("Generating root INDEX.md (Master Catalog of 232 Topics)...")
    lines = [
        "# Master Index Kurikulum — 17 Tingkat & 232 Topik Lengkap",
        "",
        "> **Repositori**: [Ultimate Learning Paths](./README.md)  ",
        "> **Cakupan**: 17 Tingkat (Tingkat 00 s/d 16) | 232 Modul Teknis Lengkap | Standar 7 Lapis Zero-to-Hero",
        "",
        "Dokumen ini adalah katalog utama dan sistem pencarian terpadu untuk seluruh materi kurikulum. Setiap modul dirancang mandiri, lengkap dengan pembuktian matematis, implementasi kode nyata, simulasi, dan rubrik proyek bertingkat.",
        "",
        "---",
        ""
    ]
    
    for tier in TIERS:
        tier_idx = tier["index"]
        tier_dir = tier["dir_name"]
        start_id, end_id = tier["topics_range"]
        tier_topics = [t for t in TOPICS_METADATA if start_id <= t[0] <= end_id]
        
        lines.extend([
            f"## [{tier['title']}](./curriculum/{tier_dir}/README.md)",
            f"> *{tier['description']}*",
            "",
            "| ID | Judul Modul Pembelajaran | Tautan Materi Langsung | Status |",
            "|:---:|---|---|:---:|"
        ])
        
        for t_id, slug, full_title, _ in tier_topics:
            filepath = f"./curriculum/{tier_dir}/{t_id:03d}-{slug}.md"
            lines.append(f"| `{t_id:03d}` | {full_title} | [Buka Modul ➡️]({filepath}) | ✅ Lengkap |")
            
        lines.append("")
        
    lines.extend([
        "---",
        "## 🧭 Panduan Navigasi & Jalur Belajar Spesialisasi",
        "- [Roadmap Prasyarat (Prerequisites DAG)](./roadmaps/prerequisites-dag.md)",
        "- [Portal Master README](./README.md)",
        "- [Panduan Metodologi Pembelajaran](./GUIDEBOOK-ID.md)",
        "- [Arsip Kurikulum Domain Lama (Side-by-Side)](./domains/)"
    ])
    
    index_path = os.path.join(BASE_DIR, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Master INDEX.md successfully generated!")

def generate_prerequisites_dag():
    print("Generating roadmaps/prerequisites-dag.md...")
    content = """# Prerequisites Directed Acyclic Graph (DAG) — Peta Ketergantungan Topik

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
- **Urutan Belajar**: Tingkat 0 $\\to$ Tingkat 1 (Aljabar Linier, Probabilitas, Optimasi) $\\to$ Tingkat 6 (Struktur Data) $\\to$ Tingkat 12 (Machine Learning, Autograd, CUDA) $\\to$ Tingkat 13 (Transformer, MoE, RLHF, Autonomous Agents).
- **Fokus Utama**: Matematika tensor, pemrograman CUDA GPU, arsitektur attention, scaling laws, dan MLOps.

### 2. Jalur Embedded Systems, Firmware & Robotics Engineer
- **Urutan Belajar**: Tingkat 0 $\\to$ Tingkat 2 (Fisika, Semikonduktor) $\\to$ Tingkat 3 (Rangkaian Listrik, MOSFET) $\\to$ Tingkat 4 (Digital Logic, CPU) $\\to$ Tingkat 5 (Bare-Metal C, DMA, RTOS) $\\to$ Tingkat 15 (Kinematika DH, PID/LQR, ROS 2, SLAM).
- **Fokus Utama**: Manipulasi bitwise, interupsi NVIC, osiloskop, kendali motor FOC, dan simulator Gazebo.

### 3. Jalur Low-Level Systems, Kernel & Security Researcher
- **Urutan Belajar**: Tingkat 0 $\\to$ Tingkat 1 (Matematika Diskrit) $\\to$ Tingkat 4 (Arsitektur Komputer x86-64/ARM) $\\to$ Tingkat 6 (Compilers, C, Memory Management) $\\to$ Tingkat 7 (Linux OS Internals, Syscalls, eBPF) $\\to$ Tingkat 11 (Kriptografi, Binary Exploitation ROP, Kernel Pwn).
- **Fokus Utama**: Disassembling Ghidra, bypass mitigasi memori, reverse engineering, dan audit kernel Linux.

### 4. Jalur Quantitative Trading, Financial Engineering & HFT
- **Urutan Belajar**: Tingkat 0 $\\to$ Tingkat 1 (Kalkulus Stokastik, Time Series, Game Theory) $\\to$ Tingkat 4 (Arsitektur CPU Cache, Bus PCIe) $\\to$ Tingkat 6 (DSA Berkinerja Tinggi) $\\to$ Tingkat 14 (Mikrostruktur Pasar LOB, Lock-Free SPSC C++, Kernel-Bypass DPDK, FPGA).
- **Fokus Utama**: Zero-allocation C++, protokol NASDAQ ITCH, persamaan Black-Scholes, dan latensi sub-mikrodetik.

---
*Kembali ke: [Master Index](../INDEX.md) | [Portal Utama](../README.md)*
"""
    dag_path = os.path.join(BASE_DIR, "roadmaps", "prerequisites-dag.md")
    with open(dag_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("roadmaps/prerequisites-dag.md successfully generated!")

def update_root_readme():
    print("Updating master portal README.md...")
    content = """# 🌌 Ultimate Learning Paths: Master Engineering & Science Encyclopedia

Selamat datang di **Ultimate Learning Paths** — sebuah sistem kurikulum sains komputasi, rekayasa perangkat keras, dan sistem rekayasa perangkat lunak paling komprehensif, terstruktur, dan mendalam. 

Kurikulum ini dirancang dari **prinsip pertama murni (first principles)** dari kondisi dasar mutlak ("seperti bayi baru lahir") hingga tingkat mahir/profesional ("mentok / production-grade"), mencakup **17 Tingkat (Tiers)** dan **232 Modul Teknis Lengkap** tanpa ada bagian yang terpotong atau terlewatkan.

---

## 🏛️ Akses Cepat & Navigasi Utama

- 📖 **[MASTER INDEX: Katalog Lengkap 232 Topik](./INDEX.md)** — Direktori sentral seluruh modul pembelajaran.
- 🗺️ **[Prerequisites Directed Acyclic Graph (DAG)](./roadmaps/prerequisites-dag.md)** — Peta jalur belajar linear dan spesialisasi karier.
- 📘 **[Panduan Metodologi Pembelajaran (ID)](./GUIDEBOOK-ID.md)** — Filosofi kognisi, active recall, dan Feynman technique.
- 📂 **[Arsip Kurikulum Domain Lama (Side-by-Side)](./domains/)** — Materi rangkuman domain terdahulu yang tetap dipertahankan.

---

## 📐 Arsitektur Kurikulum: 17 Tingkat (Tingkat 0 s/d 16)

```mermaid
flowchart LR
    subgraph Fondasi["Tahap I: Fondasi Murni & Fisika"]
        T0["Tingkat 0: Kognisi & Logika"] --> T1["Tingkat 1: Matematika"]
        T0 --> T2["Tingkat 2: Fisika & Semikonduktor"]
        T2 --> T3["Tingkat 3: Rangkaian & Elektronika"]
    end
    
    subgraph Komputer["Tahap II: Hardware & Sistem Operasi"]
        T3 --> T4["Tingkat 4: Digital Logic & CPU"]
        T4 --> T5["Tingkat 5: Embedded & RTOS"]
        T4 --> T6["Tingkat 6: CS Core & Compilers"]
        T6 --> T7["Tingkat 7: Linux OS Internals"]
    end
    
    subgraph Rekayasa["Tahap III: Komunikasi & Software Enterprise"]
        T7 --> T8["Tingkat 8: DSP & Jaringan"]
        T8 --> T9["Tingkat 9: Software Eng & SRE"]
        T9 --> T10["Tingkat 10: Basis Data Enterprise"]
        T7 --> T11["Tingkat 11: Cyber Security & Pwn"]
    end
    
    subgraph Frontier["Tahap IV: AI & Teknologi Mutakhir"]
        T1 --> T12["Tingkat 12: AI / ML / MLOps"]
        T12 --> T13["Tingkat 13: Kognisi & LLMs"]
        T6 --> T14["Tingkat 14: Fintech & HFT"]
        T5 --> T15["Tingkat 15: Robotika & Otomasi"]
        T6 --> T16["Tingkat 16: HPC & Komputasi Kuantum"]
    end
```

| Tingkat | Nama Disiplin Kurikulum | Jangkauan Modul | Fokus Inti |
|:---:|---|:---:|---|
| **0** | [Fondasi Kognitif, Logika Murni & Berpikir Ilmiah](./curriculum/00-fondasi-kognitif-logika/README.md) | Modul 001 - 005 | Meta-learning, first-principles, systems thinking, falsifikasi Karl Popper, logika formal. |
| **1** | [Fondasi Matematika Komprehensif Dari Nol](./curriculum/01-fondasi-matematika/README.md) | Modul 006 - 023 | Himpunan, aljabar linier, kalkulus multivariabel, ODE/PDE, probabilitas, optimasi, game theory. |
| **2** | [Fisika Klasik, Elektromagnetisme & Kimia Semikonduktor](./curriculum/02-fisika-semikonduktor/README.md) | Modul 024 - 037 | Mekanika Newton, termodinamika, persamaan Maxwell, optik, struktur atom, pita energi, silikon. |
| **3** | [Rangkaian Listrik, Elektronika & Microelectronics](./curriculum/03-rangkaian-mikroelektronika/README.md) | Modul 038 - 052 | Rangkaian DC/AC, BJT, MOSFET CMOS, Op-Amp, SMPS, ADC/DAC, VLSI FinFET, PCB multi-layer, SI/PI. |
| **4** | [Logika Digital, Computer Engineering & Arsitektur Komputer](./curriculum/04-logika-digital-arsitektur-komputer/README.md) | Modul 053 - 069 | Gerbang Boolean, Verilog RTL, FPGA, DRAM, RISC-V ISA, pipelining, cache MESI, MMU, akselerator GPU. |
| **5** | [Embedded Systems, Firmware Bare-Metal & RTOS / IoT](./curriculum/05-embedded-rtos-iot/README.md) | Modul 070 - 087 | ARM Cortex-M bare-metal C, linker script, DMA, FreeRTOS, Zephyr, bus CAN, Embedded Linux, TinyML. |
| **6** | [Computer Science Core, Struktur Data, Algoritma & Compiler](./curriculum/06-cs-core-dsa-compiler/README.md) | Modul 088 - 109 | Big-O, struktur data linier & pohon, graf lanjut, automata formal, Turing computability, LLVM. |
| **7** | [Operating Systems Internals & Penguasaan Penuh Linux](./curriculum/07-os-internals-linux/README.md) | Modul 110 - 124 | CPU rings, syscall dispatcher, proses fork/COW, scheduler CFS/EEVDF, VFS, io_uring, eBPF, kontainer. |
| **8** | [Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./curriculum/08-dsp-telekomunikasi-jaringan/README.md) | Modul 125 - 139 | LTI, FFT Cooley-Tukey, filter FIR/IIR, OSI, TCP/IP, BGP-4 routing, QUIC HTTP/3, SDN P4. |
| **9** | [Software Engineering, Front-End, Back-End & Cloud/SRE](./curriculum/09-software-engineering-cloud-sre/README.md) | Modul 140 - 156 | Git DAG, SOLID, arsitektur hexagonal, React Fiber, API gRPC, Kafka, Kubernetes internals, SRE. |
| **10** | [Basis Data, Data Engineering & Sistem Informasi Enterprise](./curriculum/10-basis-data-enterprise/README.md) | Modul 157 - 167 | Aljabar relasional, BCNF, B+Tree vs LSM-Tree, ACID MVCC, NoSQL, Raft konsensus, Apache Spark. |
| **11** | [Cyber Security, Kriptografi & Reverse Engineering](./curriculum/11-cybersecurity-reverse-engineering/README.md) | Modul 168 - 182 | AES-GCM, TLS 1.3, pasca-kuantum Kyber, OWASP Top 10, Ghidra reverse engineering, ROP stack pwn. |
| **12** | [Data Science, AI, Machine Learning, Deep Learning & MLOps](./curriculum/12-ai-machine-learning-mlops/README.md) | Modul 183 - 195 | Vektorisasi BLAS, regresi, autodiff PyTorch, ResNet, YOLO, Diffusion, CUDA programming, ZeRO-3. |
| **13** | [Sains Kognitif, Neuroengineering & Computational Linguistics](./curriculum/13-sains-kognitif-nlp/README.md) | Modul 196 - 206 | David Marr, Hodgkin-Huxley, BCI EEG, AlphaFold, Transformer Multi-Head Attention, RoPE, LLM RLHF. |
| **14** | [Fintech, Financial Engineering, HFT & Blockchain](./curriculum/14-fintech-hft-blockchain/README.md) | Modul 207 - 216 | Buku besar immutable, Black-Scholes, LOB matching engine, zero-allocation C++, kernel-bypass DPDK. |
| **15** | [Mekatronika, Robotika, Teori Kendali & Otomasi Industri](./curriculum/15-mekatronika-robotika-kendali/README.md) | Modul 217 - 226 | Motor BLDC FOC, sensor LiDAR, kinematika DH/Jacobian, kendali PID/LQR, Kalman Filter, ROS 2, PLC. |
| **16** | [Komputasi Performa Tinggi, Multimedia & Komputasi Kuantum](./curriculum/16-hpc-multimedia-kuantum/README.md) | Modul 227 - 232 | Grafika 3D Vulkan PBR, game engine ECS, codec video AV1, OpenMP/MPI klaster, qubit & algoritma Shor. |

---

## 💎 Standar Kualitas Modul (Template 7 Lapis)

Setiap modul dari 232 topik yang ada di repositori ini mematuhi standar format 7 lapis yang ketat:
1. **Lapis 1: Intuisi Dasar Bebas Jargon ("Seperti Bayi Baru Lahir")** — Analogi sederhana yang membumi.
2. **Lapis 2: Fondasi Teoretis & Aksiomatik / Matematis** — Rumus eksak, teorema pembuktian, dan batasan teoretis.
3. **Lapis 3: Anatomi Teknis & Cara Kerja Internal** — Mekanisme tingkat rendah, alur eksekusi, dan diagram Mermaid.
4. **Lapis 4: Implementasi Praktis & Kode / Simulasi Riil** — Kode kerja standar industri (C, Rust, Python, Verilog, SQL).
5. **Lapis 5: Miskonsepsi & Jebakan Industri** — Kesalahan umum, edge cases kritis, dan skenario crash di dunia nyata.
6. **Lapis 6: Proyek Latihan & Rubrik Penilaian Mandiri** — 3 tingkatan tantangan (Dasar, Menengah, Mahir).
7. **Lapis 7: Rekomendasi Sumber Belajar Standar Emas** — Buku teks universitas standar emas dan paper seminal klasik.

---

## 🛠️ Verifikasi Integritas Kurikulum

Untuk memastikan 100% dari 232 file topik dan link navigasi valid secara matematis, jalankan skrip verifikasi otomatis:
```bash
python scripts/verify_curriculum.py
```

---
*Dikelola dengan standar rekayasa tertinggi untuk pembelajar autodidak, ilmuwan, dan insinyur profesional masa depan.*
"""
    readme_path = os.path.join(BASE_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print("Master README.md successfully updated!")

def main():
    print("Starting Full Curriculum Build Process...")
    generate_tier_readmes()
    generate_topic_files()
    generate_master_index()
    generate_prerequisites_dag()
    update_root_readme()
    print("Full Curriculum Build Complete!")

if __name__ == "__main__":
    main()
