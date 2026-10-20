# Modul 091: Manajemen Memori & Keamanan Tipe (Pointer Manual, RAII C++, Ownership/Borrowing Rust, Garbage Collection)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 6: Tingkat 6: Computer Science Core, Struktur Data, Algoritma & Compiler](./README.md)
*Sebelumnya*: [090. ragam-mesin-eksekusi-bahasa](./090-ragam-mesin-eksekusi-bahasa.md) | *Berikutnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Selama empat dekade, dunia rekayasa perangkat lunak sistem terjebak dalam dilema abadi: Anda memilih C/C++ untuk kecepatan maksimal dengan konsekuensi mimpi buruk bug memori liar dan eksploitasi hacker, atau Anda memilih Java/Go/Python untuk keamanan memori dengan beban berat pengumpul sampah (Garbage Collector) yang menghentikan sistem sewaktu-waktu. Rekayasa Bahasa Rust ([The Rust Programming Language](https://doc.rust-lang.org/book/)) menghancurkan kompromi tersebut melalui sistem jenis yang revolusioner: **Ownership (Kepemilikan), Borrowing (Peminjaman), dan Lifetimes (Masa Hidup)**. Kompilator Rust (`rustc`) bertindak sebagai pengawas matematis yang sangat teliti pada saat kompilasi (*Borrow Checker*). Ia menjamin keamanan memori mutlak, mencegah data race pada multithreading, dan melenyapkan null pointer tanpa memerlukan Garbage Collector sama sekali. Kecepatan C dengan keamanan matematis!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Aturan Aksiomatik Sistem Kepemilikan dan Peminjaman Rust (Affine Type System):

1. **Hukum Kepemilikan (Ownership Invariants)**:
   - Setiap nilai di memori memiliki tepat satu variabel pemilik (*owner*).
   - Ketika variabel pemilik keluar dari cakupan (*scope*), nilai tersebut otomatis dihancurkan dan memori dibebaskan melalui trait `Drop`.

2. **Hukum Peminjaman dan Aliasing XOR Mutability (Borrow Checker Rule)**:
   Pada sembarang waktu dan sembarang lokasi memori $M$, Anda diizinkan memiliki:
   $$\text{Bisa: } N \times \&T \quad (\text{Banyak referensi immutable pembaca})$$
   $$\underline{\text{ATAU}} \quad 1 \times \&\text{mut } T \quad (\text{Tepat satu referensi mutable penulis})$$
   $$\text{TIDAK BISA: } \&T \land \&\text{mut } T \quad (\text{Dilarang keras aliasing bersamaan dengan mutabilitas!})$$

Formulasi Lifetimes Matematis:
Jika referensi $R$ dengan lifetime `'a` menunjuk ke data $D$ dengan lifetime `'b`, kompilator menegakkan relasi subtipe lifetime:
$$'b \supseteq 'a \quad (\text{Data } D \text{ harus hidup minimal selama referensi } R \text{ masih ada})$$

## 3. Anatomi Teknis & Cara Kerja Internal
Representasi Memori Tipe Standar Rust (`String`, `&str`, dan Fat Pointer Slices):

```mermaid
graph TD
subgraph Rust String: Owned on Stack 24-Bytes
A[ptr: Pointer ke Heap] --> D[Heap Buffer: 'H', 'e', 'l', 'l', 'o']
B[cap: Kapasitas Alokasi (misal 8)]
C[len: Panjang Karakter (5)]
end
subgraph Rust &str: Borrowed Slice Fat-Pointer 16-Bytes
E[ptr: Pointer ke Substring] --> D
F[len: Panjang Slice (misal 3)]
end
subgraph Trait Object dyn Trait: Dynamic Dispatch
G[data_ptr: Pointer ke Data Struktur]
H[vtable_ptr: Pointer ke Tabel Fungsi Virtual]
end
```

1. **Blok `unsafe` di Rust**: Rust tidak melarang akses memori tingkat rendah; Rust mengisolasi operasi berbahaya (seperti dereference raw pointer `*const T`, pemanggilan fungsi FFI C, atau manipulasi register hardware) di dalam blok eksplisit `unsafe { ... }`. Batas keamanan tetap terjaga karena pembungkus aman (*safe abstraction*) membungkus kode tidak aman tersebut ([The Rustonomicon](https://doc.rust-lang.org/nomicon/)).
2. **Fearless Concurrency**: Trait bawaan `Send` (data dapat dipindahkan kepemilikannya antar thread) dan `Sync` (referensi data dapat diakses bersamaan oleh banyak thread secara aman) otomatis diimplementasikan oleh kompilator jika seluruh anggota tipe memenuhinya.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```rust
// Safe Concurrency and Zero-Cost Abstractions in Rust
use std::sync::{Arc, Mutex};
use std::thread;

#[derive(Debug)]
struct SafeCounter {
    value: u64,
}

fn main() {
    // Arc (Atomic Reference Counting) + Mutex untuk berbagi state mutable antar thread secara aman
    let counter = Arc::new(Mutex::new(SafeCounter { value: 0 }));
    let mut handles = vec![];

    for i in 0..10 {
        let counter_clone = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            // RAII Lock: lock dilepas secara otomatis saat variabel guard keluar dari scope
            let mut guard = counter_clone.lock().expect("Mutex poisoned");
            guard.value += 1;
            println!("Thread {} incremented counter to {}", i, guard.value);
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    let final_val = counter.lock().unwrap().value;
    println!("Final Counter Value: {}", final_val);
    assert_eq!(final_val, 10);
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Borrow Checker Lifetime Annotation Hell**: Mencoba menyimpan referensi pinjaman `&'a T` di dalam struct yang kompleks alih-alih mengambil kepemilikan nilai `T` atau menggunakan `Arc<T>`. Kode akan dipenuhi anotasi lifetime yang saling mengunci dan gagal dikompilasi saat struktur bertumbuh.
2. **Deadlock akibat Penguncian Bersarang pada Mutex**: Mengambil lock Mutex B saat masih memegang lock Mutex A pada thread 1, sementara thread 2 mengambil lock Mutex A saat memegang lock Mutex B. Rust menjamin keamanan memori bebas race condition, tetapi tidak memvalidasi deadlock logika secara otomatis ([Rust Concurrency Guidelines](https://doc.rust-lang.org/book/ch16-00-concurrency.html)).
3. **Creating Dangling Raw Pointers in Unsafe Code**: Mengonversi referensi Rust menjadi raw pointer `let raw = &val as *const i32;`, membiarkan `val` dihancurkan oleh compiler, lalu melakukan dereference `unsafe { *raw }`. Hal ini melanggar kontrak invariant Rust dan menghasilkan Undefined Behavior.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis program Rust yang menerima string teks, menghitung kata terpanjang, dan mengembalikan substring sebagai referensi slice string (`&str`). Definisikan anotasi lifetime eksplisit pada tanda tangan fungsi.
2. **Tingkat Menengah**: Bangun struktur antrian antarmuka thread aman (Thread-Safe Queue) menggunakan `Arc<Mutex<VecDeque<T>>>` dan `std::sync::Condvar`. Implementasikan fungsi `push` dan fungsi `pop_blocking` yang menidurkan thread saat antrian kosong.
3. **Tingkat Mahir**: Rancang struktur data Doubly Linked List yang aman di Rust tanpa menggunakan `Rc` atau `RefCell`, melainkan mengombinasikan raw pointer `*mut Node<T>` di dalam lapisan terisolasi `unsafe`. Implementasikan trait `Drop` manual untuk membersihkan seluruh node secara iteratif dan buktikan ketiadaan kebocoran memori menggunakan `Miri` (`cargo miri test`).

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| The Rust Programming Language | Steve Klabnik & Carol Nichols | [The Rust Book](https://doc.rust-lang.org/book/) | Ownership, Borrowing, Lifetimes, Traits & Concurrency |
| The Rustonomicon: Dark Arts of Unsafe Rust | The Rust Project Developers | [The Rustonomicon](https://doc.rust-lang.org/nomicon/) | Unsafe Boundaries, Raw Pointers, Subtyping & FFI Mechanics |
| Rust for Rustaceans | Jon Gjengset | [No Starch Press Rustaceans](https://nostarch.com/rust-rustaceans) | Advanced Types, Pinning, Unsafe Invariants & Async Internals |
| Programming Rust, Second Edition | Jim Blandy, Jason Orendorff, Leonora Tindall | [O'Reilly Programming Rust](https://www.oreilly.com/library/view/programming-rust-2nd/9781492052586/) | Deep Dive Systems Programming, Memory Representation & SIMD |

---
*Navigasi Cepat*: [Ke Tingkat 6](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [090. ragam-mesin-eksekusi-bahasa](./090-ragam-mesin-eksekusi-bahasa.md) | *Berikutnya*: [092. paradigma-pemrograman-lintas-gaya](./092-paradigma-pemrograman-lintas-gaya.md)
