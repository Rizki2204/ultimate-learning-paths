# Modul 122: Model Keamanan, Izin Berkas & Identitas (User/Group, rwx, SUID/SGID, ACL, Capabilities, sudoers, systemd)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 7: Tingkat 7: Operating Systems Internals & Penguasaan Penuh Linux](./README.md)
*Sebelumnya*: [121. penguasaan-shell-terminal-mahir](./121-penguasaan-shell-terminal-mahir.md) | *Berikutnya*: [123. observabilitas-sistem-rekayasa-performa](./123-observabilitas-sistem-rekayasa-performa.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Kompilator di fase perantara boleh berkhayal memiliki triliunan variabel virtual register tanpa batas di SSA Form. Namun ketika tiba saatnya menghasilkan biner mesin fisik, dunia nyata menghantam dengan keras: prosesor x86-64 nyata hanya memiliki 16 register umum fisik, dan prosesor ARM64 hanya memiliki 31 register! Backend Kompilator & Register Allocation ([Register Allocation & Backend Engineering](https://www.cs.cmu.edu/~fp/courses/15411-f14/)) adalah seni memecahkan masalah teka-teki ruang sempit ini. Teknologi puncaknya—**Chaitin-Briggs Graph Coloring**—memetakan masalah alokasi register menjadi teka-teki mewarnai peta geografi: dua negara tetangga yang berbatasan (dua variabel yang hidup bersamaan) dilarang memiliki warna yang sama (register fisik yang sama). Jika jumlah variabel aktif melampaui jumlah register silikon fisik ($K$ warna tidak cukup), kompilator harus memilih korban secara cerdas untuk 'ditumpahkan' (**Spilling**) sementara ke memori RAM stack yang lambat.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Alokasi Register Berbasis Pewarnaan Graf Chaitin-Briggs ($K$-Coloring Graph Reduction):

Diberikan Graf Interferensi $G = (V, E)$ di mana setiap simpul $u \in V$ adalah variabel sementara (virtual register), dan sisi $(u, v) \in E$ menandakan bahwa $u$ dan $v$ hidup bersamaan (*interfere*). Target: Menemukan pewarnaan simpul dengan $K$ warna (jumlah register fisik CPU) sedemikian rupa sehingga tidak ada dua simpul bertetangga yang berwana sama.

Empat Fase Algoritma Chaitin-Briggs:
1. **Simplify**: Cari simpul $u$ dengan derajat keterhubungan $\text{deg}(u) < K$. Sesuai Teorema Kempe, jika sisa graf dapat diwarnai dengan $K$ warna, simpul $u$ pasti selalu dapat diwarnai! Hapus $u$ dari graf dan dorong ke tumpukan (*Stack*).
2. **Spill (Optimistic Spill - Briggs)**: Jika semua simpul memiliki $\text{deg} \ge K$, pilih simpul kandidat tumpah (*potential spill candidate*) berdasarkan biaya terendah:
   $$\text{Cost}(v) = \frac{\text{DefWeight}(v) + \text{UseWeight}(v) \times 10^{\text{LoopDepth}(v)}}{\text{deg}(v)}$$
   Dorong simpul kandidat ke stack dengan optimisme bahwa ia mungkin tetap dapat diwarnai nanti.
3. **Select**: Ambil simpul satu per satu dari stack dan pulihkan ke graf. Berikan warna fisik yang belum dipakai oleh tetangganya. Jika simpul potensial spill tidak mendapatkan warna yang tersedia, simpul tersebut menjadi **Actual Spill** (tambahkan instruksi simpan/muat stack memory).

Linear Scan Register Allocation (Poletto & Sarkar, 1999):
Alternatif cepat untuk Just-In-Time (JIT) Compiler dengan mengurutkan interval keaktifan secara linier dalam waktu $O(V \log V)$ alih-alih membangun graf interferensi $O(V^2)$.

## 3. Anatomi Teknis & Cara Kerja Internal
Pipeline Backend Kompilator: Dari LLVM IR ke Kode Mesin Biner Melalui Instruksi Selection & Register Allocation:

```mermaid
graph TD
A[Optimized SSA IR] --> B[Instruction Selection: SelectionDAG / GlobalISel]
B --> C[MachineInstr DAG: Virtual Register Mapping]
C --> D[Liveness Analysis: Build Interference Graph G]
D --> E[Chaitin-Briggs K-Coloring Register Allocation]
E -->|Spill Required| F[Insert Stack Spill / Reload Instructions]
E -->|Colored Successfully!| G[Map Virtual Regs to Physical CPU Regs (RAX, RBX, etc.)]
G --> H[Prolog/Epilog Insertion: Stack Frame Setup leave/ret]
H --> I[MC Layer: Emit Machine Code / ELF Object File]
end
```

1. **Instruction Selection (SelectionDAG & Tree Tiling)**: Mengubah instruksi IR abstrak menjadi instruksi prosesor fisik nyata menggunakan pencocokan pola pohon (*Maximal Munch Algorithm* atau pemrograman dinamis Burg/TableGen) ([LLVM SelectionDAG](https://llvm.org/docs/CodeGenerator.html)).
2. **Calling Convention Lowering**: Menyisipkan instruksi penyimpanan register *callee-saved* dan pemulihan frame stack pada pembukaan (*prologue*) dan penutupan (*epilogue*) fungsi.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Chaitin-Briggs K-Coloring Register Allocator Simplification Phase in Python
from typing import Dict, Set, List

class RegisterAllocator:
    def __init__(self, adj_matrix: Dict[str, Set[str]], num_physical_regs: int):
        self.adj = {k: set(v) for k, v in adj_matrix.items()}
        self.k = num_physical_regs
        self.stack: List[str] = []
        self.spill_list: List[str] = []

    def simplify(self):
        while self.adj:
            # 1. Cari simpul dengan derajat keterhubungan < K
            low_degree_nodes = [node for node, neighbors in self.adj.items() if len(neighbors) < self.k]
            
            if low_degree_nodes:
                # Pilih satu simpul untuk dihapus dan didorong ke stack
                node = low_degree_nodes[0]
                self.stack.append(node)
                # Hapus simpul dan seluruh sisinya dari graf sementara
                for neighbor in self.adj[node]:
                    self.adj[neighbor].discard(node)
                del self.adj[node]
            else:
                # 2. Kemacetan: Semua simpul berderajat >= K -> Pilih simpul untuk Spilling!
                spill_candidate = max(self.adj.keys(), key=lambda n: len(self.adj[n]))
                self.spill_list.append(spill_candidate)
                self.stack.append(spill_candidate)
                for neighbor in self.adj[spill_candidate]:
                    self.adj[neighbor].discard(spill_candidate)
                del self.adj[spill_candidate]

        print(f"Simplification complete! Stack order: {self.stack}")
        print(f"Spill candidates: {self.spill_list}")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Spill Code Explosion Inside Inner Loops**: Memilih variabel sementara yang sering diakses di dalam loop terdalam sebagai korban tumpahan (*Spill*). Setiap iterasi loop akan melakukan operasi lambat pembacaan dan penulisan memori stack RAM, menghancurkan performa biner kompilasi.
2. **Register Allocation Coalescing Conflicts**: Menggabungkan dua variabel hasil copy (`a = b`) menjadi satu register tanpa memeriksa apakah penggabungan tersebut meningkatkan derajat simpul tetangga melampaui $K$ (Gunakan kriteria Briggs atau George Coalescing).
3. **Ignoring Hardware Register Constraints (ABI Clashing)**: Mengalokasikan sembarang register tanpa memperhitungkan bahwa beberapa instruksi prosesor memiliki register khusus yang dipatok keras oleh silikon (seperti operasi pembagian x86 `idiv` yang wajib menggunakan pasangan `%rax:%rdx`).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Gambarkan Graf Interferensi untuk 5 variabel dengan interval keaktifan: $A: [0, 3], B: [1, 4], C: [2, 5], D: [4, 6], E: [5, 7]$. Tentukan apakah graf tersebut dapat diwarnai dengan $K=2$ register tanpa spilling.
2. **Tingkat Menengah**: Implementasikan fase pemilihan warna (*Select Phase*) pada Chaitin-Briggs allocator di Python: ambil simpul dari stack dan tetapkan warna $1 \dots K$. Jika simpul tidak bisa diwarnai, tandai sebagai actual spill.
3. **Tingkat Mahir**: Implementasikan Algoritma Linear Scan Register Allocation (Poletto & Sarkar) untuk $K = 4$ register fisik. Buktikan algoritma selesai dalam waktu linier $O(N \log N)$ pada sekumpulan 10.000 interval keaktifan sintetis.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Register Allocation via Coloring | Gregory J. Chaitin (IBM Research) | [Chaitin 1981 Classic Paper](https://dl.acm.org/doi/10.1016/0890-5401%2882%2990035-7) | Makalah Orisinal Penemuan Graph Coloring Register Allocation |
| Register Allocation via Coloring (Briggs Thesis) | Preston Briggs (Rice University) | [Briggs Ph.D. Thesis 1992](https://www.cs.utexas.edu/users/mckinley/380C/lecs/briggs-thesis-1992.pdf) | Optimistic Coloring, Rematerialization & Conservative Coalescing |
| Linear Scan Register Allocation | Massimiliano Poletto & Vivek Sarkar | [ACM TOPLAS 1999 Paper](https://dl.acm.org/doi/10.1145/330249.330250) | Algoritma Linear Scan Cepat untuk JIT Virtual Machines |
| The LLVM Target-Independent Code Generator | The LLVM Team | [LLVM CodeGen Guide](https://llvm.org/docs/CodeGenerator.html) | SelectionDAG, FastISel, LiveIntervals & Greedy Register Allocator |

---
*Navigasi Cepat*: [Ke Tingkat 7](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [121. penguasaan-shell-terminal-mahir](./121-penguasaan-shell-terminal-mahir.md) | *Berikutnya*: [123. observabilitas-sistem-rekayasa-performa](./123-observabilitas-sistem-rekayasa-performa.md)
