# Modul 139: Software-Defined Networking / SDN & Otomasi Jaringan (OpenFlow, P4, VXLAN Overlay, Netmiko, Wireshark)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 8: Tingkat 8: Pemrosesan Sinyal Digital, Telekomunikasi & Network Engineering](./README.md)
*Sebelumnya*: [138. keamanan-infrastruktur-jaringan-lanjut](./138-keamanan-infrastruktur-jaringan-lanjut.md) | *Berikutnya*: [140. siklus-hidup-pengembangan-perangkat-lunak](../09-software-engineering-cloud-sre/140-siklus-hidup-pengembangan-perangkat-lunak.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Jika dua orang teman di belahan dunia yang berbeda mengunggah foto ke media sosial, foto siapa yang diunggah lebih dulu? Anda mungkin tergoda untuk melihat jam di pojok layar komputer masing-masing. Namun di dunia sistem terdistribusi, jam fisik komputer adalah pembohong besar: kristal kuarsa di dalam setiap server berdetak pada kecepatan yang sedikit berbeda akibat suhu dan usia komponen (**Clock Drift**), membuat jam mereka berselisih beberapa milidetik atau detik. Waktu Fisik vs Logis Sistem Terdistribusi ([Logical Time & TrueTime Architecture](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)) adalah seni mengurutkan kausalitas tanpa bergantung pada jam dinding: Leslie Lamport menciptakan **Jam Logis (Lamport Timestamps)** dan **Vector Clocks** yang mendefinisikan waktu murni berdasarkan hubungan sebab-akibat (*Happened-Before*); sementara Google membangun **TrueTime API** untuk database global Spanner menggunakan antena satelit GPS militer dan jam atom cesium di setiap data center untuk menaklukkan ketidakpastian waktu fisik!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Relasi Sebab-Akibat Leslie Lamport (Happened-Before Relation $\to$) dan Vector Clocks:

1. **Relasi Happened-Before ($\to$)**:
   Dua peristiwa $a$ dan $b$ dalam sistem terdistribusi memenuhi $a \to b$ jika dan hanya jika:
   - $a$ dan $b$ terjadi pada proses yang sama, dan $a$ terjadi sebelum $b$.
   - $a$ adalah peristiwa pengiriman pesan oleh satu proses, dan $b$ adalah peristiwa penerimaan pesan tersebut oleh proses lain.
   - Terdapat peristiwa $c$ sedemikian rupa sehingga $a \to c$ dan $c \to b$ (Sifat Transitif).
   Jika $a \not\to b$ dan $b \not\to a$, maka peristiwa $a$ dan $b$ terjadi secara **Bersamaan (Concurrent: $a \parallel b$)**.

2. **Algoritma Vector Clocks (Fidge & Mattern, 1988)**:
   Setiap node $i$ dari total $N$ node memelihara vektor integer $V_i[1 \dots N]$:
   - Sebelum mengeksekusi peristiwa internal: $V_i[i] = V_i[i] + 1$.
   - Saat mengirim pesan $m$: kirim vektor $V_i$ bersama pesan.
   - Saat menerima pesan $m$ dengan vektor $V_{msg}$:
     $$V_i[j] = \max(V_i[j], \ V_{msg}[j]) \quad \forall j \in [1, N]$$
     $$V_i[i] = V_i[i] + 1$$
   Aturan Perbandingan Kausalitas:
   $$V_a < V_b \iff (\forall k, V_a[k] \le V_b[k]) \land (\exists k, V_a[k] < V_b[k]) \iff a \to b$$

3. **Google Spanner TrueTime API**:
   TrueTime merepresentasikan waktu fisik bukan sebagai satu angka pasti, melainkan sebagai rentang interval ketidakpastian:
   $$TT.now() = [t_{earliest}, \ t_{latest}] \quad \text{dengan margin galat } \epsilon = \frac{t_{latest} - t_{earliest}}{2} \approx 1-7\text{ ms}$$
   Prinsip *Commit Wait*: Sebelum meng-commit transaksi, server sengaja menunggu selama $2\epsilon$ milidetik untuk menjamin secara absolut bahwa stempel waktu transaksi berikutnya pasti berada di masa depan waktu fisik!

## 3. Anatomi Teknis & Cara Kerja Internal
Perbandingan Pelacakan Urutan Kausalitas: Jam Fisik vs Lamport Timestamp vs Vector Clocks:

```mermaid
graph LR
subgraph Node 1
A[Event e1: V=[1,0,0]] -->|Send Msg 1 with V=[1,0,0]| B[Event e2: V=[2,0,0]]
end
subgraph Node 2
C[Event e3: Receives Msg 1 -> Updates V=[1,1,0]] --> D[Event e4: V=[1,2,0]]
end
subgraph Node 3 (Independent Concurrent Event)
E[Event e5: V=[0,0,1]]
end
A -.->|Causally Precedes| C
E -.->|Concurrent e5 || e4: Conflict Detected!| D
```

1. **Keterbatasan Lamport Timestamps**: Lamport Timestamps ($L(a) < L(b)$) menjamin bahwa *jika $a \to b$, maka $L(a) < L(b)$*. Namun kebalikannya TIDAK berlaku: jika $L(a) < L(b)$, kita TIDAK BISA menyimpulkan bahwa $a \to b$ (bisa jadi keduanya concurrent!). Vector Clocks memecahkan masalah ini dengan memberikan jaminan hubungan dua arah yang sempurna ([Lamport Clocks Original Paper](https://lamport.azurewebsites.net/pubs/time-clocks.pdf)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Complete Vector Clock Implementation and Causality Checker in Python
from typing import List, Tuple

class VectorClock:
    def __init__(self, node_id: int, num_nodes: int):
        self.node_id = node_id
        self.clock = [0] * num_nodes

    def tick(self):
        self.clock[self.node_id] += 1

    def send_event(self) -> List[int]:
        self.tick()
        return list(self.clock)

    def receive_event(self, received_vector: List[int]):
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], received_vector[i])
        self.clock[self.node_id] += 1

    @staticmethod
    def compare(v1: List[int], v2: List[int]) -> str:
        v1_le = all(x <= y for x, y in zip(v1, v2))
        v2_le = all(y <= x for x, y in zip(v1, v2))
        if v1_le and not v2_le: return "HAPPENED_BEFORE (v1 -> v2)"
        if v2_le and not v1_le: return "HAPPENED_AFTER (v2 -> v1)"
        if v1 == v2: return "IDENTICAL"
        return "CONCURRENT (Conflict / Forked!)"

print("Vector clock causality engine initialized!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **Last-Write-Wins (LWW) Data Silent Destruction**: Menggunakan jam dinding fisik NTP untuk menyelesaikan konflik pembaruan data secara naif ('data dengan timestamp jam terbesar yang menang'). Karena clock drift server, data yang diubah 5 detik kemudian bisa terhapus oleh data lama yang servernya memiliki jam fisik yang lebih cepat!
2. **Vector Clock Size Explosion on Dynamic Membership**: Memelihara vector clocks pada sistem peer-to-peer dengan jutaan pengguna dinamis yang sering bergabung dan keluar. Vektor jam akan membesar hingga megabyte per objek data (solusi: gunakan Dotted Version Vectors atau Interval Tree pruning).
3. **NTP Leap Second Panic**: Ketika protokol NTP menyisipkan satu detik kabisat (Leap Second) dengan mengulang detik 23:59:59 dua kali. Server Linux yang tidak menggunakan *Leap Smearing* akan melihat waktu bergerak mundur, memicu kepanikan deadlock pada kernel scheduler dan database.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Simulasikan 3 proses yang bertukar 4 pesan dengan Lamport Timestamps. Hitung nilai timestamp akhir setiap proses dan tunjukkan urutan total parsial yang dihasilkan.
2. **Tingkat Menengah**: Gunakan kelas `VectorClock` di atas untuk mensimulasikan skenario cabang konflik paralel (*Forked Edit*): Node A mengedit dokumen, Node B mengedit dokumen yang sama tanpa mengetahui aksi Node A. Buktikan fungsi `compare` mendeteksi status `CONCURRENT`.
3. **Tingkat Mahir**: Rancang simulasi algoritma Google TrueTime Commit-Wait di Python. Tunjukkan bahwa dengan menyisipkan delay $2\epsilon$ pada setiap operasi commit transaksi, serializability transaksi global dapat dicapai tanpa perlu mengunci database di seluruh dunia.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Time, Clocks, and the Ordering of Events in a Distributed System | Leslie Lamport | [ACM Communications 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf) | Makalah Paling Banyak Dikutip di CS: Happened-Before, Logical Clocks |
| Spanner: Google's Globally-Distributed Database | James C. Corbett et al. (Google) | [Google Spanner OSDI 2012 Paper](https://research.google/pubs/pub39966/) | TrueTime API, GPS/Atomic Clocks, Commit-Wait & External Consistency |
| Designing Data-Intensive Applications (DDIA) | Martin Kleppmann | [DDIA Official Portal](https://dataintensive.net/) | Bab 8 & 9: Unreliable Clocks, Monotonic Clocks, Linearizability & Total Order |
| Timestamps in Message-Passing Systems That Preserve the Partial Ordering | Colin Fidge & Friedemann Mattern | [Vector Clocks Original Paper](https://link.springer.com/chapter/10.1007/978-3-642-88544-0_24) | Penemuan Struktur Vektor Jam Terdistribusi & Deteksi Konkurensi |

---
*Navigasi Cepat*: [Ke Tingkat 8](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [138. keamanan-infrastruktur-jaringan-lanjut](./138-keamanan-infrastruktur-jaringan-lanjut.md) | *Berikutnya*: [140. siklus-hidup-pengembangan-perangkat-lunak](../09-software-engineering-cloud-sre/140-siklus-hidup-pengembangan-perangkat-lunak.md)
