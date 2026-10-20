# -*- coding: utf-8 -*-
"""
Canonical realignment mapping for Tiers 6 - 11 (Topics 88 - 182).
Resolves all topic index misalignments and integrates missing topics.
"""

from scripts.encyclopedia.tier_6_part1 import DATA_TIER_6_PART1 as t6p1
from scripts.encyclopedia.tier_6_part2 import DATA_TIER_6_PART2 as t6p2
from scripts.encyclopedia.tier_7_part1 import DATA_TIER_7_PART1 as t7p1
from scripts.encyclopedia.tier_7_part2 import DATA_TIER_7_PART2 as t7p2
from scripts.encyclopedia.tier_8_part1 import DATA_TIER_8_PART1 as t8p1
from scripts.encyclopedia.tier_8_part2 import DATA_TIER_8_PART2 as t8p2
from scripts.encyclopedia.tier_9_part1 import DATA_TIER_9_PART1 as t9p1
from scripts.encyclopedia.tier_10_part1 import DATA_TIER_10_PART1 as t10p1
from scripts.encyclopedia.tier_11_part1 import DATA_TIER_11_PART1 as t11p1

from scripts.encyclopedia.missing_tier_6 import DATA_MISSING_TIER_6 as m6
from scripts.encyclopedia.missing_tier_7 import DATA_MISSING_TIER_7 as m7
from scripts.encyclopedia.missing_tier_8 import DATA_MISSING_TIER_8 as m8
from scripts.encyclopedia.missing_tier_9 import DATA_MISSING_TIER_9 as m9
from scripts.encyclopedia.missing_tier_10 import DATA_MISSING_TIER_10 as m10
from scripts.encyclopedia.missing_tier_11 import DATA_MISSING_TIER_11 as m11

CANONICAL_TIERS_6_11 = {
    # === TIER 6 (88 - 109): CS Core, Data Structures, Algorithms & Compilers ===
    88: m6[88],      # Data representation: ASCII, Unicode, UTF-8, Endianness
    89: t6p1[88],    # Execution lifecycle: Preprocessing, Compiling, Linking, ELF, Memory layout
    90: t7p2[124],   # Execution engines: Native, Bytecode VM JVM/CLR, JIT V8
    91: t6p1[90],    # Memory management & type safety: Pointers, RAII, Rust ownership, GC
    92: t6p1[91],    # Programming paradigms: Imperative, OOP, Functional, Data-oriented
    93: t6p1[92],    # Complexity analysis: Asymptotic Big-O, Master Theorem, Amortized
    94: t6p1[93],    # Linear data structures: Dynamic Array, Linked Lists, Stack, Queue
    95: t6p1[96],    # Hash-based data structures: Hash functions, SipHash, Collision resolution
    96: t6p2[98],    # Tree data structures: BST, AVL, Red-Black Tree, B-Tree
    97: t6p2[97],    # Priority queues & Heaps: Binary Heap, Fibonacci Heap
    98: m6[98],      # String & prefix data structures: Trie, Radix Tree, Suffix Array
    99: m6[99],      # Disjoint-set & range data structures: DSU, Segment Tree, Fenwick
    100: m6[100],    # Probabilistic data structures: Bloom Filter, Skip List, HyperLogLog
    101: t6p2[100],  # Graph representations: Adjacency Matrix, Adjacency List
    102: t6p2[99],   # Sorting & searching algorithms: QuickSort, MergeSort, Binary Search
    103: t6p2[103],  # Classic algorithm paradigms: Dynamic Programming, Divide & Conquer
    104: t6p2[101],  # Advanced graph algorithms: Dijkstra, Bellman-Ford, A*, Kruskal, Tarjan
    105: m6[105],    # String & computational geometry: KMP, Aho-Corasick, Convex Hull
    106: t7p2[116],  # Formal language & automata: DFA, NFA, Regex, CFG, Chomsky hierarchy
    107: m6[107],    # Computability theory: Turing machine, Halting problem, Rice's theorem
    108: m6[108],    # Computational complexity: P, NP, NP-Complete, Karp reductions
    109: t7p2[123],  # Compiler & interpreter engineering: Lexer, Parser, AST, SSA IR, LLVM

    # === TIER 7 (110 - 124): Linux & OS Internals ===
    110: m7[110],    # OS history & evolution: Multics, Unix philosophy, Microkernel vs Monolithic
    111: t7p1[105],  # CPU Privilege rings: Kernel space vs User space, Traps, Interrupts
    112: t7p1[106],  # Syscall interface: Dispatch table, vDSO acceleration
    113: m7[113],    # Linux boot process: UEFI, GPT, GRUB2, Vmlinuz, Initramfs, systemd
    114: t7p1[107],  # Process management: task_struct, fork, COW, execve, zombie
    115: m7[115],    # CPU scheduling: CFS vruntime, EEVDF, Real-time SCHED_FIFO/RR
    116: t7p1[109],  # Kernel concurrency & sync: Spinlock, Mutex, Futex, RCU
    117: t7p1[108],  # Inter-process communication: Pipes, Signals, Shared memory, Unix sockets
    118: t7p1[110],  # Virtual memory management: Paging, Page fault, Buddy allocator, SLUB
    119: t7p1[112],  # VFS & Storage: Superblock, Inode, Dentry, File descriptors, ext4
    120: t7p1[111],  # High-speed I/O: epoll, io_uring, non-blocking I/O
    121: m7[121],    # Advanced shell & terminal: Bash/Zsh, pipelines, grep, sed, awk, jq
    122: t7p1[113],  # Security model: User/Group, Permissions, Capabilities, SUID
    123: t7p1[114],  # System observability & profiling: vmstat, strace, perf, eBPF
    124: t7p1[115],  # Kernel isolation & containerization: Namespaces, cgroups v2, chroot, OverlayFS

    # === TIER 8 (125 - 139): DSP, Telecommunications & Computer Networks ===
    125: t8p1[125],  # Signals & systems: Continuous vs Discrete, LTI, Convolution
    126: t8p1[126],  # Frequency domain transforms: Fourier, CTFT, DTFT, FFT, Laplace, Z
    127: m8[127],    # Digital filter design: FIR linear-phase, IIR bilinear transform
    128: t8p1[127],  # Physical telecommunications & channels: AM/FM, QAM/OFDM, Shannon capacity
    129: m8[129],    # Channel error detection & correction: CRC, Hamming, Reed-Solomon, LDPC
    130: m8[130],    # Physical transmission media & propagation: Copper, Optical fiber, RF
    131: m8[131],    # Advanced wireless communications: Massive MIMO, Beamforming, 5G NR
    132: t8p1[129],  # Computer networks: OSI model & TCP/IP stack encapsulation
    133: t8p1[130],  # Layer 2 Data Link: Ethernet frames, MAC learning, STP/RSTP, VLAN
    134: t8p1[131],  # Layer 3 Network: IPv4, CIDR, VLSM, ARP, ICMP, NAT, IPv6
    135: t8p1[132],  # Layer 3 Routing: OSPF, BGP-4 internet backbone, MPLS
    136: t8p1[133],  # Layer 4 Transport: UDP, TCP handshake, Flow control, CUBIC, BBR, QUIC
    137: t8p2[135],  # Layer 7 Application: DHCP, DNS/DNSSEC, HTTP/1.1 s/d HTTP/3
    138: m8[138],    # Network infrastructure security: Firewalls, IDS/IPS, WireGuard, DDoS
    139: t8p2[137],  # SDN & network automation: OpenFlow, P4, DPDK kernel bypass

    # === TIER 9 (140 - 156): Software Engineering, Cloud & SRE ===
    140: m9[140],    # SDLC, Agile, Scrum, Kanban, RFC, ADR, Technical debt
    141: t9p1[151],  # Advanced Git: DAG architecture, Merge vs Rebase, Reflog
    142: t9p1[146],  # Clean code & design patterns: SOLID principles, 23 GoF patterns
    143: t9p1[148],  # Large-scale software architecture: Clean/Hexagonal, Microservices, DDD
    144: t9p1[152],  # Automated testing methodologies: Test pyramid, Unit, Integration, TDD
    145: m9[145],    # HCI & UI/UX: Fitts's law, Hick's law, WCAG AAA accessibility
    146: m9[146],    # Front-End browser engine: DOM/CSSOM render tree, V8 event loop, WebAssembly
    147: m9[147],    # Front-End modern UI frameworks: React Fiber, Svelte signals, SSR, Vite
    148: m9[148],    # Mobile & desktop cross-platform engineering: Flutter, React Native, Tauri
    149: t9p1[150],  # Back-End HTTP server architecture & APIs: RESTful, GraphQL, gRPC
    150: m9[150],    # Back-End security authentication & authorization: Argon2, JWT, OAuth 2.0
    151: t8p2[144],  # Multi-tier caching strategies: Redis, Consistent hashing, Cache stampede
    152: t8p2[145],  # Asynchronous message processing: RabbitMQ, Apache Kafka, Outbox pattern
    153: t8p2[138],  # Distributed systems resilience: 8 Fallacies, Circuit breakers, Rate limiting
    154: t9p1[153],  # DevOps, Cloud infrastructure & Platform engineering: CI/CD, Terraform
    155: t9p1[154],  # Container orchestration: Kubernetes control plane, Pods, Services
    156: t9p1[156],  # Observability & SRE: Prometheus, Grafana, OpenTelemetry, SLI/SLO

    # === TIER 10 (157 - 167): Databases & Enterprise Systems ===
    157: m10[157],   # Database theoretical foundations: Relational algebra, ERD
    158: m10[158],   # Normalization theory: 1NF to BCNF, Controlled denormalization
    159: m10[159],   # Advanced SQL: Complex joins, Recursive CTEs, Window functions
    160: t10p1[158], # Storage engine internals: Slotted pages, B+Tree, LSM-Tree, WAL
    161: t10p1[157], # Query optimization & execution: Cost-Based Optimizer, EXPLAIN ANALYZE
    162: t10p1[160], # ACID transactions & concurrency control: 2PL, MVCC, ARIES recovery
    163: t10p1[162], # Non-relational databases: Redis, MongoDB, Cassandra, Vector DB
    164: t8p2[141],  # Distributed databases & global consensus: Raft, Paxos, Quorum
    165: t10p1[164], # Data engineering & bulk data processing: Iceberg, Parquet, Apache Spark
    166: m10[166],   # Enterprise management information systems: ERP, CRM, SCM, TOGAF, ITIL
    167: m10[167],   # Enterprise datacenter hardware infrastructure: Tier I-IV, PUE, SAN/NAS

    # === TIER 11 (168 - 182): Cybersecurity, Cryptography & Reverse Engineering ===
    168: t11p1[169], # Classical cryptography: CIA triad, Cryptographic entropy, CSPRNG
    169: m11[169],   # Stream ciphers & perfect secrecy: One-Time Pad, ChaCha20
    170: t11p1[170], # Block ciphers & modes: AES Rijndael, ECB pitfalls, CBC, GCM AEAD
    171: t11p1[172], # Cryptographic hash functions: SHA-256, SHA-3, BLAKE3, HMAC
    172: t11p1[171], # Asymmetric cryptography: Trapdoor functions, RSA, Diffie-Hellman, ECC
    173: t11p1[173], # Public key infrastructure: X.509 CA, Chain of trust, TLS 1.3
    174: t11p1[180], # Advanced cryptography: zk-SNARKs, Post-quantum lattice Kyber
    175: m11[175],   # Offensive security: Reconnaissance, Nmap SYN scan, Kerberoasting
    176: t11p1[174], # Offensive security: Web & API exploitation, OWASP Top 10, SQLi, XSS
    177: t11p1[177], # Reverse engineering & binary analysis: Disassembly, ELF/PE, Ghidra
    178: t11p1[175], # Low-level memory exploitation / Pwn: Stack buffer overflow, ROP, UAF
    179: t11p1[176], # Memory exploitation mitigations: Stack Canary, ASLR, DEP/NX
    180: m11[180],   # Linux kernel exploitation & hardware hacking: commit_creds, firmware SPI
    181: t11p1[182], # Defensive security, Blue Team & SOC: Zero-Trust, SIEM, threat modeling
    182: t11p1[179], # Digital forensics & incident response: NIST IR, Volatility, Autopsy
}
