# Modul 163: Basis Data Non-Relasional / NoSQL (Redis In-Memory, MongoDB Document, Cassandra Wide-Column, Qdrant Vector DB)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 10: Tingkat 10: Basis Data, Data Engineering & Sistem Informasi Enterprise](./README.md)
*Sebelumnya*: [162. transaksi-acid-kontrol-konkurensi-lanjut](./162-transaksi-acid-kontrol-konkurensi-lanjut.md) | *Berikutnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika Anda mencoba menemukan hubungan pertemanan 5 derajat di Facebook ('Teman dari teman dari teman dari teman dari teman saya') menggunakan database relasional SQL biasa, Anda harus menulis kueri SQL dengan 5 kali operasi `JOIN` raksasa pada tabel berisi miliaran baris. Database SQL Anda akan berasap dan mati kehabisan memori CPU karena kompleksitas komputasinya meledak secara eksponensial. Database Graf (Graph Databases) ([Graph Databases & Neo4j](https://neo4j.com/developer/graph-database/)) lahir untuk menaklukkan hubungan keterhubungan rumit ini: alih-alih mencari data melalui tabel indeks perantara yang mahal, setiap simpul entitas (Node) memegang pointer memori fisik langsung ke simpul-simpul tetangganya (**Index-Free Adjacency**)! Menelusuri jejaring sosial miliaran orang berubah dari pencarian tabel lambat $O(N)$ menjadi lompatan pointer instan $O(1)$ per langkah, secepat kilat melintasi graf pengetahuan dunia!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Model Graf Properti (Labeled Property Graph / LPG) dan Formalisme Index-Free Adjacency (IFA):

1. **Model Graf Properti (LPG)**:
   Didefinisikan secara formal sebagai tupel 7 elemen:
   $$G = (V, E, L_V, L_E, P_V, P_E, \delta)$$
   - $V$: Himpunan simpul entitas (*Nodes / Vertices*).
   - $E$: Himpunan hubungan terarah (*Edges / Relationships*).
   - $L_V, L_E$: Label klasifikasi kategori simpul dan relasi (misal `:Person`, `:FOLLOWS`).
   - $P_V, P_E$: Properti pasangan kunci-nilai yang disematkan langsung di dalam simpul atau relasi.
   - $\delta: E \to V \times V$: Pemetaan arah hubungan dari simpul sumber ke simpul target.

2. **Index-Free Adjacency (IFA) vs Relational Foreign Key Joins**:
   - **RDBMS SQL Join**: Memeriksa indeks B+ Tree pada setiap lompatan relasi: $T(d) = O(d \times \log |V|)$ atau $O(|V| \cdot |E|)$. Waktu kueri melambat seiring membesarnya ukuran total database global!
   - **Native Graph Database (IFA)**: Setiap simpul menyimpan alamat memori pointer langsung dari simpul-simpul tetangganya: $T(d) = O(k^d)$ di mana $k$ adalah rata-rata derajat cabang tetangga lokal. **Waktu kueri benar-benar independen dari ukuran total database global!**

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur Struktur File Penyimpanan Asli Neo4j di Disk (Fixed-Size Record Files):

```mermaid
graph LR
subgraph Node Record File neostore.nodestore.db: Fixed 15 Bytes
N1[InUse: 1B | NextRelId: 4B | NextPropId: 4B | Extra: 6B]
end
subgraph Relationship Record File neostore.relationshipstore.db: Fixed 34 Bytes
R1[InUse: 1B | FirstNode: 4B | SecondNode: 4B | RelType: 2B | PrevRelNode1: 4B | NextRelNode1: 4B | PrevRelNode2: 4B | NextRelNode2: 4B]
end
N1 -->|Direct Offset Pointer Calculation: id * 34| R1
```

1. **Fixed-Size Records Pointer Arithmetic**: Karena setiap record simpul berukuran persis 15 byte dan setiap relasi berukuran persis 34 byte, Neo4j dapat menghitung alamat byte fisik disk dari simpul ke-$X$ secara instan tanpa indeks: $\text{Address} = X \times 15\text{ bytes}$! Pembacaan disk melesat pada batas kecepatan hardware.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Index-Free Adjacency (IFA) In-Memory Graph Traversal Simulator in Python
from typing import List, Dict

class GraphNode:
    def __init__(self, node_id: int, label: str, name: str):
        self.id = node_id
        self.label = label
        self.name = name
        # Index-Free Adjacency: Pointer referensi memori langsung ke tetangga!
        self.outgoing_edges: List['GraphEdge'] = []

class GraphEdge:
    def __init__(self, rel_type: str, target_node: GraphNode):
        self.rel_type = rel_type
        self.target = target_node # Pointer langsung ke objek memori berikutnya

# Traversal O(1) per langkah tanpa lookup tabel indeks!
def find_friends_of_friends(start_node: GraphNode) -> List[str]:
    fof_names = []
    for edge1 in start_node.outgoing_edges:
        if edge1.rel_type == "FRIEND":
            friend = edge1.target
            for edge2 in friend.outgoing_edges:
                if edge2.rel_type == "FRIEND" and edge2.target != start_node:
                    fof_names.append(edge2.target.name)
    return fof_names

print("Index-free adjacency graph traversal engine loaded!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Dense Node / Supernode Graph Explosion**: Sebuah simpul selebriti memiliki 10 juta sisi relasi (`:FOLLOWED_BY`). Setiap kali kueri melintasi simpul supernode ini, traversal melambat hingga ribuan milidetik (solusi: terapkan relasi bertingkat hierarkis atau partisi sisi).
2. **Abusing Graph Databases for Tabular Relational Workloads**: Menggunakan database graf untuk kueri agregasi tabular sederhana (seperti `SELECT AVG(salary) FROM employees`). Database graf tidak dioptimasi untuk pemindaian kolom skalar massal.
3. **Graph Partitioning Bottleneck in Distributed Clusters**: Memecah satu graf properti besar ke ratusan server jaringan terpisah. Banyak traversal lompatan sisi yang terpaksa melintasi jaringan antar server (*Cross-Network Edge Hopping*), menghancurkan keunggulan performa latensi lokal Index-Free Adjacency.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis kueri bahasa graf Cypher untuk membuat dua simpul `:Person` bernama 'Budi' dan 'Siti' yang dihubungkan oleh relasi `:KNOWS` dengan properti `since: 2024`.
2. **Tingkat Menengah**: Bangun sistem deteksi penipuan transaksi keuangan (Fraud Detection) sederhana di Python menggunakan model graf: deteksi cincin pencucian uang melingkar (*Circular Money Laundering*: Rekening A -> Rekening B -> Rekening C -> Rekening A) menggunakan algoritma deteksi siklus graf.
3. **Tingkat Mahir**: Rancang mesin database graf native minimal di C++ menggunakan slotted memory blocks berukuran tetap (16 byte per node record, 32 byte per relationship record). Implementasikan kueri pencarian rute terpendek dua arah (*Bidirectional Breadth-First Search*) langsung di atas pointer file disk.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Graph Databases: New Opportunities for Connected Data | Ian Robinson, Jim Webber, Emil Eifrem (Neo4j) | [Neo4j Free O'Reilly Book](https://neo4j.com/graph-databases-book/) | Alkitab Database Graf: LPG Model, Index-Free Adjacency & Cypher Patterns |
| The Neo4j Native Graph Engine Architecture | Neo4j Engineering Team | [Neo4j Developer Documentation](https://neo4j.com/developer/graph-database/) | Storage Engine Internals, Record Files, Pointer Chasing & Caching Layers |
| The Property Graph Schema and Query Language (GQL Standard) | ISO/IEC Joint Technical Committee | [ISO GQL Standard 2024](https://www.iso.org/standard/76388.html) | Standar Internasional Resmi Bahasa Kueri Graf Deklaratif GQL |
| Designing Data-Intensive Applications (Graph-Like Data Models) | Martin Kleppmann | [DDIA Graph Models Chapter](https://dataintensive.net/) | Analisis Komparasi Model Relasional vs Dokumen vs Graf Properti & Triple-Stores |

---
*Navigasi Cepat*: [Ke Tingkat 10](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [162. transaksi-acid-kontrol-konkurensi-lanjut](./162-transaksi-acid-kontrol-konkurensi-lanjut.md) | *Berikutnya*: [164. basis-data-terdistribusi-konsensus-global](./164-basis-data-terdistribusi-konsensus-global.md)
