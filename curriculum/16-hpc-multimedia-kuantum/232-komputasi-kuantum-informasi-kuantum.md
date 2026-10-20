# Modul 232: Komputasi Kuantum & Ilmu Informasi Kuantum (Qubit Superposisi, Keterikatan Bell, Gerbang Kuantum Hadamard/CNOT, Algoritma Shor)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 16: Tingkat 16: Komputasi Performa Tinggi, Multimedia & Komputasi Kuantum](./README.md)
*Sebelumnya*: [231. komputasi-performa-tinggi-hpc-supercomputing](./231-komputasi-performa-tinggi-hpc-supercomputing.md) | *Berikutnya*: *Puncak Kurikulum (Tuntas 100%)*

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Komputer klasik Anda memproses bit informasi seperti saklar lampu biasa: ia hanya bisa berada dalam kondisi MATI (0) atau HIDUP (1). Jika Anda mencari jalan keluar dari labirin dengan 1 juta cabang, komputer klasik harus mencoba setiap cabang satu per satu secara berurutan. Komputer Kuantum menggunakan fenomena aneh fisika sub-atomik: sebuah Qubit (Quantum Bit) dapat berada dalam kondisi 0 DAN 1 SEKALIGUS (Superposisi)! Melalui interferensi kuantum, komputer kuantum dapat menjelajahi seluruh 1 juta cabang labirin tersebut secara bersamaan dan memperkuat gelombang jawaban yang benar!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Status Keadaan Kuantum Qubit Murni (Superposisi):
$$|\psi\rangle = \alpha |0\rangle + \beta |1\rangle, \quad \alpha, \beta \in \mathbb{C}, \quad |\alpha|^2 + |\beta|^2 = 1$$
Di mana $|0\rangle = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ dan $|1\rangle = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ adalah vektor basis komputasional ortonormal pada Bola Bloch (*Bloch Sphere*).

Keterikatan Kuantum (Quantum Entanglement) - Pasangan Status Bell:
$$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$
Jika qubit pertama diukur bernilai $|0\rangle$, maka qubit kedua seketika runtuh (*instantaneous collapse*) ke status $|0\rangle$ dengan probabilitas 100%, tidak peduli seberapa jauh jarak fisik kedua qubit tersebut (aksi jarak jauh Einstein: *spooky action at a distance*).

Gerbang Logika Kuantum Elementer:
- **Hadamard Gate ($H$)**: Menciptakan superposisi sempurna dari status basis:
  $$H = \frac{1}{\sqrt{2}} \begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}, \quad H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$
- **Controlled-NOT (CNOT)**: Membalik target qubit jika dan hanya jika control qubit bernilai $|1\rangle$.

Algoritma Faktorisasi Shor:
Mampu memfaktorkan bilangan bulat $N$ dalam kompleksitas waktu polinomial kuantum $\tilde{O}((\log N)^3)$ menggunakan Transformasi Fourier Kuantum (QFT), yang secara teoretis meruntuhkan seluruh sistem kriptografi kunci publik klasik RSA modern.

## 3. Anatomi Teknis & Cara Kerja Internal
Hardware Qubit Fisik (Superconducting Transmon Qubits pada IBM/Google Quantum AI): Sirkuit superkonduktor berbasis sambungan Josephson didinginkan hingga suhu $15\text{ mK}$ (hampir nol mutlak) menggunakan Dilution Refrigerator untuk mencegah dekoherensi termal dari getaran atom lingkungan sekitarnya.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
import numpy as np

# Simulasi Simulator Keadaan Kuantum Vektor Status (Statevector)
def quantum_hadamard():
    return (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]])

def quantum_cnot():
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])

# 1. Mulai dengan 2 Qubit dalam status dasar |00>
psi_00 = np.array([1.0, 0.0, 0.0, 0.0]) # Representasi |00>

# 2. Terapkan Gerbang Hadamard pada Qubit 0 (H (tensor) I)
H = quantum_hadamard()
I = np.eye(2)
H_tensor_I = np.kron(H, I)
psi_superposition = np.dot(H_tensor_I, psi_00)

# 3. Terapkan Gerbang CNOT untuk menciptakan Status Keterikatan Bell (Bell State)
CNOT = quantum_cnot()
bell_state = np.dot(CNOT, psi_superposition)

print("Vektor Keadaan Pasangan Bell (|00> + |11>) / sqrt(2):")
print(np.round(bell_state, 4))
prob_00 = np.abs(bell_state[0])**2
prob_11 = np.abs(bell_state[3])**2
print(f"Probabilitas Pengukuran |00>: {prob_00:.1f} | Probabilitas |11>: {prob_11:.1f}")
print("Status terbukti terikat kuantum murni: Pengukuran Qubit A langsung menentukan Qubit B!")
```

## 5. Miskonsepsi & Jebakan Industri
No-Cloning Theorem: hukum fisika kuantum melarang keras penyalinan status kuantum yang tidak diketahui ($|\psi\rangle$) menjadi status identik kedua. Konsekuensinya: kita tidak bisa membuat backup atau salinan variabel qubit seperti variabel biasa di pemrograman klasik; koreksi kesalahan kuantum harus menggunakan teknik Quantum Error Correction (Surface Codes) dengan overhead ribuan physical qubit per 1 logical qubit.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Representasikan status qubit di koordinat bola Bloch menggunakan sudut rotasi $\theta$ dan $\phi$. Level 2: Buat sirkuit kuantum teleportasi sederhana menggunakan SDK Qiskit di Python. Level 3: Rancang algoritma pencarian Grover untuk membuktikan keunggulan kuadratik kuantum $O(\sqrt{N})$ atas pencarian klasik $O(N)$.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information (10th Anniversary ed.)*. Cambridge University Press.
- Preskill, J. (2018). *Quantum Computing in the NISQ era and beyond*. Quantum, 2, 79.

---
*Navigasi Cepat*: [Ke Tingkat 16](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [231. komputasi-performa-tinggi-hpc-supercomputing](./231-komputasi-performa-tinggi-hpc-supercomputing.md) | *Berikutnya*: *Puncak Kurikulum (Tuntas 100%)*
