# Modul 155: Orkestrasi Kontainer: Bedah Internal Kubernetes (K8s Control Plane, Pods, Deployments, Services, Ingress, Istio)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [154. devops-cloud-infrastructure-platform-engineering](./154-devops-cloud-infrastructure-platform-engineering.md) | *Berikutnya*: [156. observabilitas-tiga-pilar-sre](./156-observabilitas-tiga-pilar-sre.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
### 1.1 Konsep Inti & Analogi Tanpa Jargon
Di masa lalu, menginstal aplikasi server adalah siksaan: Anda membutuhkan pustaka Python versi 3.9, tetapi sistem operasi server hanya menyediakan versi 3.6; dan jika Anda memperbarui pustaka sistem, aplikasi lain yang berjalan di server yang sama akan crash (*Dependency Hell*). Virtualisasi & Container Orchestration ([Docker & Kubernetes Architecture](https://kubernetes.io/docs/concepts/overview/)) telah melenyapkan kutukan 'Tapi di laptop saya jalan!' untuk selamanya. **Docker** mengemas aplikasi Anda bersama seluruh pustaka dan konfigurasinya ke dalam kotak kontainer standar yang dijamin berjalan identik di laptop pengembang maupun di ribuan server cloud. Dan ketika Anda memiliki 10.000 kontainer yang berjalan serentak, **Kubernetes (K8s)** bertindak sebagai kapten kapal armada otomatis raksasa: ia memantau kontainer yang mati dan menghidupkannya kembali dalam hitungan detik (**Self-Healing**), menaikkan jumlah kontainer saat pengunjung melonjak (**Autoscaling**), dan mendistribusikan lalu lintas secara merata tanpa ada server yang kelebihan beban.

### 1.2 Urgensi Rekayasa & Signifikansi Sistemik
Dalam rekayasa sistem modern, pemahaman mendalam tentang konsep ini membedakan arsitek sistem kelas dunia dari sekadar operator perkakas teknis.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
### 2.1 Kerangka Teori Aksiomatik & Formulasi Matematis
Arsitektur Kontroler Terdistribusi Kubernetes (Control Plane vs Worker Nodes) dan Status Deklaratif:

### 2.2 Penurunan Matematis Langkah-demi-Langkah
Filosofi Inti Kubernetes: **Declarative Desired State vs Current Actual State**.
Operator tidak memberi instruksi imperatif langkah-demi-langkah; operator mendeklarasikan status yang diinginkan dalam file YAML (misal: *'Saya ingin 5 buah pod berjalan'*). Loop Rekonsiliasi Pengontrol (*Reconciliation Control Loop*) terus-menerus membandingkan status aktual dengan status deklarasi:

$$\text{Loop Rekonsiliasi}: \quad \text{Reconcile}() \implies \begin{cases} \text{Do Nothing} & \text{Actual} == \text{Desired} \\ \text{Spawn / Terminate Pods} & \text{Actual} \ne \text{Desired} \end{cases}$$

Komponen Inti Control Plane Kubernetes:
1. **`kube-apiserver`**: Pintu gerbang REST API tunggal yang memvalidasi dan mengonfigurasi seluruh objek pod/service.
2. **`etcd`**: Database Key-Value terdistribusi berbasis konsensus Raft yang menyimpan seluruh status kebenaran klaster.
3. **`kube-scheduler`**: Menentukan di worker node fisik mana pod baru harus ditempatkan berdasarkan ketersediaan CPU dan RAM.
4. **`kube-controller-manager`**: Menjalankan daemon pengendali (DeploymentController, ReplicaSetController).

Komponen Worker Node Fisik:
- **`kubelet`**: Agen kapten node yang berkomunikasi dengan container runtime (Containerd via CRI).
- **`kube-proxy`**: Mengelola aturan firewall virtual iptables/IPVS untuk pengalihan Service IP.

## 3. Anatomi Teknis & Cara Kerja Internal
Hierarki Objek Orkestrasi Kubernetes: Dari Deployment ke Container RunTime:

```mermaid
graph TD
A[Deployment: Rolling Update Strategy & Version Control] --> B[ReplicaSet: Ensures exact N replicas]
B --> C[Pod 1: Smallest Deployable Unit IP Address & Shared Volume]
B --> D[Pod 2: Replica]
C --> E[Container 1: App Service]
C --> F[Container 2: Sidecar Logging/Proxy]
G[Service ClusterIP: Stable Virtual IP & Internal Load Balancer] --> C
G --> D
end
```

1. **Pod Network Model (CNI - Container Network Interface)**:
   Setiap Pod mendapatkan alamat IP unik yang dapat dirutekan di seluruh klaster (*Every Pod gets its own IP*). Pod dapat berkomunikasi dengan semua pod lain di node mana pun tanpa NAT port-mapping melalui jaringan overlay (Calico, Cilium berbasis eBPF) ([Kubernetes Network Model](https://kubernetes.io/docs/concepts/services-networking/)).

#### Tabel Penelusuran Siklus CrashLoopBackOff & Pengusiran Pod Kubernetes (Cascading Eviction)
| Siklus Rekonsiliasi Kubelet | Status Kontainer Pod | Konsumsi Memori Aktual vs Limit | Sinyal Kernel OS yang Dipicu | Kebijakan Restart Kubelet (*BackOff*) | Status Node Kluster Kubernetes |
|---|---|---|---|---|---|
| Inisialisasi Pod | Menjalankan aplikasi | $50\text{ MB} / 512\text{ MB}$ (Limit) | - | Status `Running` | Node stabil |
| Kebocoran Memori Heap | Alokasi data tanpa batas | Naik ke $510\text{ MB} / 512\text{ MB}$ | Mendekati batas cgroup `memory.max`| - | Kubelet memantau cgroup |
| Batas Terlampaui | Alokasi melebihi 512 MB | $513\text{ MB} > 512\text{ MB}$ | **KERNEL OOM-KILLER MENGIRIM SIGKILL (137)!**| Kontainer mati mendadak | Exit Code: 137 (OOMKilled) |
| Siklus CrashLoop | Kubelet me-restart pod | Memori bocor berulang | Mati lagi dalam 10 detik | Waktu jeda restart eksponensial ($10\text{s} \to 300\text{s}$)| Status: `CrashLoopBackOff` |
| Pengusiran Berantai | 50 Pod OOM bersamaan | Kubelet kehabisan memori node fisik | Tekanan memori node (*MemoryPressure*) | Kubelet mulai mengusir pod lain (*Eviction*)| Pod sehat ikut terusir! |
| Mitigasi Arsitektur | Penyesuaian Request/Limit | Profiling memori presisi & HPA | Deteksi kebocoran memori dini | Pod direstart sebelum batas node terancam | Kluster kembali stabil |

## 4. Implementasi Praktis & Kode / Simulasi Riil
```yaml
# Production-Grade Kubernetes Deployment and Service Manifest (deployment.yaml)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telemetry-api-deployment
  labels:
    app: telemetry-api
spec:
  replicas: 3 # Menjamin selalu ada tepat 3 Pod yang hidup mandiri
  selector:
    matchLabels:
      app: telemetry-api
  template:
    metadata:
      labels:
        app: telemetry-api
    spec:
      containers:
      - name: api-server
        image: telemetry-api:v1.2.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "250m" # 0.25 CPU Core jaminan minimum
            memory: "256Mi"
          limits:
            cpu: "1000m" # 1.0 CPU Core batas maksimum
            memory: "512Mi" # Mencegah Pod memakan seluruh RAM node!
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

## 5. Miskonsepsi & Jebakan Industri
1. **Omitting Resource Requests and Limits**: Menyebarkan Pod ke Kubernetes tanpa mendefinisikan `resources.limits.memory`. Jika satu pod mengalami memory leak, pod tersebut akan menyedot seluruh RAM fisik node host, memicu OOM Killer kernel membunuh pod-pod penting tetangga (*Noisy Neighbor Problem*).
2. **Confusing Liveness and Readiness Probes**: Mengarahkan Liveness Probe ke pemeriksaan database eksternal. Jika database downstream lambat atau down, seluruh pod Kubernetes akan menganggap dirinya rusak dan melakukan restart serentak (*Restart Death Spiral*), melumpuhkan klaster.
3. **Running Root Containers in Production**: Menjalankan kontainer dengan pengguna bawaan `root` (UID 0). Jika penyerang berhasil melakukan container breakout, penyerang langsung memiliki hak istimewa superuser pada host fisik.

### Studi Kasus Kegagalan Nyata: Reaksi Berantai Pengusiran Pod dan Keruntuhan Kluster Kubernetes Akibat OOMKilled Cascading Eviction
- **Kronologi & Konteks Kasus**: Pada platform streaming video global yang berjalan di atas kluster Kubernetes dengan ribuan node, peluncuran versi mikroservis rekomendasi baru memicu pengusiran pod (*pod eviction*) massal yang menyebar ke seluruh kluster, meruntuhkan ratusan node komputasi dan memicu pemadaman layanan selama lebih dari dua jam.
- **Akar Masalah Orkestrasi Kontainer, cgroups, & Kubelet Eviction Thresholds**: Pengembang mengonfigurasi batas memori kontainer (*Memory Limit*) yang sama persis dengan batas permintaan memori (*Memory Request*), namun kode baru memuat kebocoran memori (*Memory Leak*) yang cepat. Ketika penggunaan memori kontainer menyentuh batas cgroup, kernel Linux mengeksekusi OOM Killer dengan sinyal `SIGKILL 137` (*OOMKilled*). Kubelet mencoba me-restart pod tersebut berulang kali, masuk ke status `CrashLoopBackOff`. Karena puluhan pod yang bocor berjalan pada node pekerja fisik yang sama, akumulasi alokasi memori menembus ambang batas keselamatan node (*Kubelet Hard Eviction Threshold / memory.available < 100Mi*). Kubelet menandai node dengan status `MemoryPressure` dan mulai mengusir (*evict*) seluruh pod lain yang ada di node tersebut secara paksa. Pod-pod yang terusir dijadwalkan ulang oleh Kubernetes Scheduler ke node tetangga yang sehat, memindahkan beban memori bocor dan memicu reaksi berantai pengusiran node tetangga (*Cascading Eviction Storm*) hingga seluruh kluster kehabisan kapasitas.

- **Potongan Kode / Arsitektur Cacat (Vulnerable Implementation)**:
```yaml
# Rekonstruksi Cacat Konfigurasi Pod Kubernetes yang Memicu OOMKilled
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leaky-recommendation-service
spec:
  replicas: 50
  template:
    spec:
      containers:
      - name: app
        image: recommendation:v2.1-leaky
        resources:
          requests:
            memory: "512Mi" # KESALAHAN: Request terlalu mepet dengan limit
            cpu: "250m"
          limits:
            memory: "512Mi" # Saat menyentuh 512Mi: KERNEL OOM KILLER MENGIRIM SIGKILL (Exit 137)!
        # Ketiadaan Liveness Probe yang tepat menunda deteksi kebocoran memori
```

- **Analisis Forensik & Rekayasa Modern**: Insiden Cascading Eviction mengajarkan pentingnya pemahaman interaksi antara orkestrator kontainer dan subsistem kernel host. Standar arsitektur Kubernetes modern mewajibkan: (1) Penerapan *Quality of Service* (QoS) Class yang tepat (Guaranteed vs Burstable); (2) Konfigurasi *Horizontal Pod Autoscaler* (HPA) dan *Vertical Pod Autoscaler* (VPA) yang menyesuaikan alokasi sumber daya secara dinamis; (3) Pemasangan *PriorityClass* dan *PodDisruptionBudgets* (PDB) yang melindungi pod infrastruktur kritis dari pengusiran sembarangan saat node mengalami tekanan memori.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Bangun file `Dockerfile` multi-stage untuk aplikasi web, bangun image kontainer lokal dengan `docker build`, dan jalankan kontainer dengan pembatasan memori (`docker run -m 256m`).
2. **Tingkat Menengah**: Pasang klaster Kubernetes lokal (menggunakan Minikube, Kind, atau K3s). Terapkan manifes Deployment 3 replika di atas, lalu matikan salah satu pod secara manual (`kubectl delete pod <name>`) dan amati bagaimana Kubernetes Controller secara otomatis menghidupkan pod baru dalam 1 detik.
3. **Tingkat Mahir**: Konfigurasikan Horizontal Pod Autoscaler (HPA) berbasis metrik utilisasi CPU: gunakan alat benchmarking beban kueri HTTP (`hey` atau `wrk`) untuk membanjiri deployment dan amati bagaimana Kubernetes secara otomatis menskalakan pod dari 3 menjadi 10 replika secara dinamis.

### Tingkat 1: Dasar
- **Tugas**: Bangun manifes deklaratif Kubernetes (YAML) lengkap untuk aplikasi web stateless berkeandalan tinggi yang memuat Deployment (3 replika, strategi `RollingUpdate` dengan `maxSurge: 1` dan `maxUnavailable: 0`), Service bertipe `ClusterIP`, penegakan kuota `resources` (requests dan limits), serta konfigurasi pemeriksaan kesehatan *Liveness Probe* dan *Readiness Probe* berbasis HTTP endpoint.
- **Petunjuk Perancangan Arsitektur**:
  - Readiness probe memverifikasi kesiapan koneksi basis data sebelum menerima lalu lintas.
  - Liveness probe mendeteksi apakah proses mengalami deadlock/hang dan me-restart kontainer otomatis.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Validasi Skema*: Uji manifes dengan utilitas linter `kubeval` atau `kubectl --dry-run=client`; pastikan seluruh atribut mematuhi skema OpenAPI Kubernetes resmi tanpa peringatan sintaks.
- **Rubrik Penilaian Mandiri**: 40% Kelengkapan Manifes Kubernetes Sesuai Praktik Terbaik, 30% Konfigurasi Liveness/Readiness Probe yang Tepat, 30% Strategi RollingUpdate Bebas Downtime.

### Tingkat 2: Menengah
- **Tugas**: Kembangkan pengontrol rekonsiliasi mini (*Custom Kubernetes Controller / Operator Loop*) dalam Python/Go menggunakan pola *Informer & Workqueue* yang memantau pembuatan objek kustom (*Custom Resource Definition / CRD*), membandingkan status aktual terhadap status yang diinginkan, dan secara otomatis membuat Pod baru jika jumlah replika fisik kurang dari spesifikasi.
- **Petunjuk Perancangan Arsitektur**:
  - Terapkan fungsi rekonsiliasi idempoten: `Reconcile(Request) -> Result`.
  - Gunakan mekanisme exponential backoff pada workqueue saat terjadi kegagalan pembaruan status.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Simulasi Self-Healing*: Hapus 1 Pod yang dikelola operator secara manual via API; buktikan kontroler mendeteksi penyimpangan status (*drift*) dan membuat 1 Pod pengganti baru secara otomatis dalam waktu $< 2\text{ detik}$.
- **Rubrik Penilaian Mandiri**: 40% Arsitektur Reconciliation Loop Controller yang Tepat, 30% Sifat Idempoten Rekonsiliasi Status CRD, 30% Kemampuan Self-Healing Terverifikasi.

### Tingkat 3: Mahir
- **Tugas**: Rancang webhook penerimaan mutasi dan validasi (*Admission Webhook Server*) dalam Go/Python untuk Kubernetes API Server yang memeriksa setiap Pod yang akan dibuat di kluster, menolak pembuatan Pod jika tidak memiliki batas memori (*Memory Limits Validation*), dan secara otomatis menyuntikkan kontainer pendamping keamanan (*Security Sidecar Container Injection*) ke dalam spesifikasi Pod sebelum disimpan ke etcd.
- **Petunjuk Perancangan Arsitektur**:
  - Bangun endpoint HTTPS bertipe `MutatingAdmissionWebhook` dan `ValidatingAdmissionWebhook`.
  - Hasilkan patch mutasi dalam format JSONPatch (RFC 6902) untuk menyuntikkan kontainer sidecar.
- **Test Vector & Kasus Uji Ekstrem**:
  - *Penolakan Pod Cacat*: Ajukan pembuatan Pod tanpa field `resources.limits`; buktikan webhook menolak pembuatan Pod dengan pesan: `Admission denied: Seluruh kontainer wajib memiliki memory limit!`.
- **Rubrik Penilaian Mandiri**: 40% Kepatuhan Protokol AdmissionReview Kubernetes API, 30% Penyusunan Mutasi JSONPatch RFC 6902 yang Presisi, 30% Penegakan Kebijakan Keamanan Kluster.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Kubernetes Documentation: Concepts and Architecture | The Kubernetes Authors (CNCF) | [Kubernetes Official Docs](https://kubernetes.io/docs/concepts/overview/) | Pods, Services, Deployments, Controller Loops & Networking Models |
| Kubernetes Up & Running: Dive into the Future of Infrastructure | Kelsey Hightower, Brendan Burns, Joe Beda | [O'Reilly Kubernetes Book](https://www.oreilly.com/library/view/kubernetes-up-and/9781098110192/) | Ditulis oleh Para Pencipta Asli K8s: Pod Lifecycle, Storage & Ingress |
| Containerd Architecture and Core Design | CNCF Containerd Project | [Containerd Official Portal](https://containerd.io/) | OCI Runtime Standards, CRI Plugins, Snapshotters & Shim Architecture |
| Production Kubernetes: Building Robust Systems | Josh Rosso et al. (VMware) | [O'Reilly Production K8s](https://www.oreilly.com/library/view/production-kubernetes/9781492092292/) | Multi-Cluster Networking, Cilium eBPF CNI, RBAC Security & Disaster Recovery |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [154. devops-cloud-infrastructure-platform-engineering](./154-devops-cloud-infrastructure-platform-engineering.md) | *Berikutnya*: [156. observabilitas-tiga-pilar-sre](./156-observabilitas-tiga-pilar-sre.md)
