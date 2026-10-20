# Modul 221: Dinamika Robot, Perencanaan Gerak & Trajektori (Formulasi Dinamika Euler-Lagrange, Mobile Robot Kinematics, RRT* Planner)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 15: Tingkat 15: Mekatronika, Robotika, Teori Kendali & Otomasi Industri](./README.md)
*Sebelumnya*: [220. representasi-spasial-3d-kinematika](./220-representasi-spasial-3d-kinematika.md) | *Berikutnya*: [222. teori-kendali-klasik](./222-teori-kendali-klasik.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Mengetahui posisi sudut sendi robot (kinematika) barulah setengah cerita. Jika sebuah lengan robot memegang beban besi seberat 20 kg dan bergerak cepat, hukum inersia Newton dan gaya sentrifugal akan mencoba membengkokkan lengan tersebut ke samping. Berapa torsi motor yang harus dikerahkan oleh masing-masing sendi agar gerakan lengan tetap mulus dan tidak patah?

Inilah ranah **Dinamika Robot** ([Murray, Li, Sastry - A Mathematical Introduction to Robotic Manipulation](https://www.cse.lehigh.edu/~trac/teaching/cse360/MurrayLiSastry94.pdf)). Menggunakan persamaan mekanika analitik **Euler-Lagrange**, kita bisa memperhitungkan seluruh massa, inersia putaran, gaya Coriolis, dan gaya gravitasi di setiap milidetik lintasan.

Dan ketika robot mobil otonom (seperti robot pembersih lantai atau mobil tanpa supir) harus melintasi labirin kantor yang penuh kursi dan meja berantakan dari lobi ke ruang rapat, bagaimana ia merencanakan jalurnya?

Algoritma pencarian grid biasa akan meledak komputasinya di ruang berdimensi tinggi. Ilmuwan robotika menggunakan **Rapidly-exploring Random Trees (RRT / RRT\*)**: algoritma pencarian probabilistik yang menembakkan cabang-cabang pohon acak ke seluruh penjuru ruangan seperti jaring laba-laba, lalu menyambungkannya menjadi jalur terpendek bebas tabrakan dalam sekejap mata ([LaValle & Kuffner - Randomized Kinodynamic Planning](https://ieeexplore.ieee.org/document/925726)).

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Dinamika Manipulator & Perencanaan RRT\*:

1. **Persamaan Gerak Dinamika Manipulator Euler-Lagrange**:
Dituliskan dalam bentuk matriks kanonikal standar:
$$M(q) \ddot{q} + C(q, \dot{q}) \dot{q} + g(q) = \tau$$
Di mana:
* $q, \dot{q}, \ddot{q} \in \mathbb{R}^n$ adalah posisi, kecepatan, dan percepatan sudut sendi.
* $M(q) \in \mathbb{R}^{n \times n}$ adalah matriks inersia sendi yang simetris dan definit positif ($M(q) = M(q)^T > 0$).
* $C(q, \dot{q}) \in \mathbb{R}^{n \times n}$ adalah matriks gaya Coriolis dan sentrifugal (memenuhi sifat anti-simetris $\dot{M} - 2C = -(\dot{M} - 2C)^T$).
* $g(q) \in \mathbb{R}^n$ adalah vektor gaya torsi gravitasi: $g_i(q) = \frac{\partial V(q)}{\partial q_i}$.
* $\tau \in \mathbb{R}^n$ adalah vektor torsi aktuator pengendali ([Craig Robotics Chapter 6](https://www.pearson.com/en-us/subject-catalog/p/introduction-to-robotics-mechanics-and-control/P200000003314)).

2. **Kinematika Non-Holonomik Robot Bergerak Roda Diferensial**:
Robot bergerak dengan dua roda independen berjarak $L$ dan jari-jari roda $r$:
Kendali kecepatan maju linier $v$ dan kecepatan sudut belok $\omega$:
$$\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix} \cos\theta & 0 \\ \sin\theta & 0 \\ 0 & 1 \end{bmatrix} \begin{bmatrix} v \\ \omega \end{bmatrix}$$
Kendala non-holonomik murni (tidak ada slip lateral roda ke samping): $\dot{x}\sin\theta - \dot{y}\cos\theta = 0$.

3. **Algoritma Perencanaan Jalur Optimal Asimtotik RRT\***:
Secara iteratif mengambil sampel status acak $q_{\text{rand}} \in \mathcal{C}_{\text{free}}$, mencari simpul terdekat $q_{\text{nearest}}$, melangkah sejauh $\Delta t$ ke $q_{\text{new}}$.
*Koneksi Ulang Optimal (Rewiring Step)*: Memeriksa tetangga dalam radius bola $r = \gamma \left(\frac{\log n}{n}\right)^{1/d}$, menyambungkan simpul yang meminimalkan total biaya akumulasi jalur, menjamin konvergensi jalur optimal terpendek hampir pasti seiring $n \to \infty$ ([Karaman & Frazzoli - Sampling-based Algorithms for Optimal Motion Planning](https://arxiv.org/abs/1105.1186)).

## 3. Anatomi Teknis & Cara Kerja Internal
Arsitektur siklus pembaruan pohon probabilistik RRT\* dengan rewiring lokal:

```mermaid
flowchart TD
    Sample["Sampel Titik Acak q_rand di C_free"] --> Nearest["Cari Simpul Terdekat q_nearest dalam Pohon"]
    Nearest --> Steer["Steering Function: Melangkah sejauh epsilon -> q_new"]
    Steer --> Collision{"Bebas Tabrakan Rintangan?"}
    
    Collision -- Tidak --> Sample
    Collision -- Ya --> NearNodes["Identifikasi Himpunan Tetangga Q_near dalam Radius r"]
    
    NearNodes --> ChooseParent["Pilih Simpul Induk Terbaik: min(Cost(q_near) + Dist(q_near, q_new))"]
    ChooseParent --> AddEdge["Tambahkan Edge ke Pohon"]
    AddEdge --> Rewire["Rewiring: Periksa apakah jalur tetangga via q_new lebih murah!"]
    Rewire --> CheckGoal{"Mencapai Zona Tujuan?"}
    CheckGoal -- Belum --> Sample
    CheckGoal -- Ya --> Path["Ekstrak Jalur Bebas Tabrakan Optimal"]
```

Dengan langkah *Rewiring*, RRT\* terus-menerus meluruskan cabang-cabang pohon yang berkelok-kelok, membedakannya dari RRT biasa yang menghasilkan jalur zigzag yang kasar ([Karaman & Frazzoli 2011](https://arxiv.org/abs/1105.1186)).

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

# 1. Implementasi Sederhana Algoritma Rapidly-exploring Random Tree (RRT) 2D
class RRTPlanner:
    def __init__(self, start, goal, obstacles, bounds=(0, 100), step_size=5.0):
        self.start = np.array(start)
        self.goal = np.array(goal)
        self.obstacles = obstacles # List tuple: (x, y, radius)
        self.bounds = bounds
        self.step_size = step_size
        self.tree = [self.start]
        self.parent = {0: None}
        
    def plan(self, max_iter=1000):
        for i in range(max_iter):
            # 10% Goal-biased sampling
            if np.random.rand() < 0.1:
                q_rand = self.goal
            else:
                q_rand = np.random.uniform(self.bounds[0], self.bounds[1], size=2)
                
            # Cari simpul terdekat
            dists = [np.linalg.norm(q_rand - node) for node in self.tree]
            nearest_idx = np.argmin(dists)
            q_nearest = self.tree[nearest_idx]
            
            # Melangkah sejauh step_size
            diff = q_rand - q_nearest
            dist = np.linalg.norm(diff)
            if dist == 0:
                continue
            q_new = q_nearest + (diff / dist) * min(self.step_size, dist)
            
            # Pengecekan Tabrakan dengan Rintangan Lingkaran
            collision = False
            for ox, oy, r in self.obstacles:
                if np.linalg.norm(q_new - np.array([ox, oy])) <= r:
                    collision = True
                    break
                    
            if not collision:
                new_idx = len(self.tree)
                self.tree.append(q_new)
                self.parent[new_idx] = nearest_idx
                
                # Cek jika mencapai target
                if np.linalg.norm(q_new - self.goal) <= self.step_size:
                    # Rekonstruksi Jalur
                    path = [self.goal, q_new]
                    curr = nearest_idx
                    while curr is not None:
                        path.append(self.tree[curr])
                        curr = self.parent[curr]
                    return path[::-1]
        return None

# Uji Coba Perencanaan Jalur RRT
planner = RRTPlanner(
    start=(5, 5),
    goal=(90, 90),
    obstacles=[(40, 40, 15), (60, 70, 12)], # 2 Rintangan besar
    bounds=(0, 100),
    step_size=4.0
)

np.random.seed(42)
path = planner.plan(max_iter=2000)
print(f"Status Perencanaan Jalur: {'SUKSES DITEMUKAN' if path else 'GAGAL'}")
print(f"Jumlah Titik Lintasan   : {len(path)} waypoints")
print(f"Koordinat Awal: {path[0]} -> Koordinat Akhir: {path[-1]}")
```

## 5. Miskonsepsi & Jebakan Industri
*Inversi Matriks Inersia pada Komputasi Dinamika Maju*: Menghitung percepatan sendi $\ddot{q} = M(q)^{-1} (\tau - C\dot{q} - g)$ dengan melakukan invers matriks eksplisit berukuran $n \times n$ membutuhkan biaya $\mathcal{O}(n^3)$ yang sangat lambat untuk lengan dengan banyak derajat kebebasan. Gunakan algoritma rekursif **Recursive Newton-Euler Algorithm (RNEA)** untuk dinamika invers ($\mathcal{O}(n)$) dan **Articulated-Body Algorithm (ABA)** Roy Featherstone untuk dinamika maju ($\mathcal{O}(n)$ linier murni) ([Featherstone - Rigid Body Dynamics Algorithms](https://link.springer.com/book/10.1007/978-0-387-74315-8)).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
### Level 1 (Pemula)
Tulis simulasi model kinematika diferensial robot mobil beroda dua (Unicycle Model) di Python: berikan input kecepatan maju konstan $v = 1.0\text{ m/s}$ dan kecepatan belok $\omega = 0.5\text{ rad/s}$ selama 10 detik, dan plot lintasan lingkaran sempurna yang terbentuk di bidang 2D.
*Rubrik*: Lintasan membentuk kurva lingkaran dengan radius $R = v / \omega = 2.0\text{ meter}$.

### Level 2 (Menengah)
Implementasikan perencana trajektori polinomial derajat-5 (*Quintic Polynomial Trajectory*) untuk pergerakan sendi tunggal yang menjamin percepatan awal dan akhir nol (menghilangkan sentakan jerk):
$$q(t) = a_0 + a_1 t + a_2 t^2 + a_3 t^3 + a_4 t^4 + a_5 t^5$$
Tentukan koefisien $a_0 \dots a_5$ dari kondisi batas posisi, kecepatan, dan percepatan awal/akhir.
*Rubrik*: Plot grafik posisi, kecepatan, dan percepatan mulus tanpa lonjakan diskontinu.

### Level 3 (Mahir)
Bangun implementasi algoritma RRT\* lengkap dengan fungsi pemilihan induk minimum dan rewiring lokal berjejari adaptif di Python: uji coba pada labirin dengan koridor sempit (*narrow passage*), bandingkan panjang jalur total terhadap RRT biasa, dan buktikan penurunan biaya jalur seiring bertambahnya iterasi.
*Rubrik*: Panjang lintasan RRT\* minimal $15\%$ lebih pendek daripada RRT standar.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Sampling-based Algorithms for Optimal Motion Planning (RRT*) | Sertac Karaman & Emilio Frazzoli (MIT) | [arXiv RRT* Paper](https://arxiv.org/abs/1105.1186) | Bukti Asimtotik Optimalitas RRT*, Rewiring Algoritma |
| Rigid Body Dynamics Algorithms | Roy Featherstone | [Springer Link Classic](https://link.springer.com/book/10.1007/978-0-387-74315-8) | Algoritma Dinamika Rekursif Newton-Euler RNEA & ABA O(n) |
| Planning Algorithms | Steven M. LaValle (UIUC) | [Cambridge Planning Algorithms Book](http://lavalle.pl/planning/) | Alkitab Perencanaan Gerak Robot, Ruang Konfigurasi C-Space |
| A Mathematical Introduction to Robotic Manipulation | Richard M. Murray, Zexiang Li, S. Shankar Sastry | [CRC Press Free PDF](https://www.cse.lehigh.edu/~trac/teaching/cse360/MurrayLiSastry94.pdf) | Formulasi Formal Dinamika Manipulator Euler-Lagrange |

---
*Navigasi Cepat*: [Ke Tingkat 15](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [220. representasi-spasial-3d-kinematika](./220-representasi-spasial-3d-kinematika.md) | *Berikutnya*: [222. teori-kendali-klasik](./222-teori-kendali-klasik.md)
