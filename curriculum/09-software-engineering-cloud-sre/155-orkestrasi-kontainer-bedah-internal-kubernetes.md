# Modul 155: Orkestrasi Kontainer: Bedah Internal Kubernetes (K8s Control Plane, Pods, Deployments, Services, Ingress, Istio)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [154. devops-cloud-infrastructure-platform-engineering](./154-devops-cloud-infrastructure-platform-engineering.md) | *Berikutnya*: [156. observabilitas-tiga-pilar-sre](./156-observabilitas-tiga-pilar-sre.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Menjalankan ribuan aplikasi kontainer di cloud seperti mengelola ratusan kapal kontainer raksasa di pelabuhan tersibuk di dunia. Siapa yang memastikan kapal tidak saling bertabrakan? Siapa yang memindahkan muatan jika satu kapal bocor dan tenggelam di tengah malam? Kubernetes adalah nahkoda pelabuhan otonom: Anda cukup menulis deklarasi 'Saya ingin 10 salinan aplikasi toko online selalu aktif', dan Kubernetes akan terus memantau, menghidupkan kembali pod yang mati, dan mendistribusikan beban secara otomatis!

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Arsitektur Control Plane & Node Kubernetes:
1. **Control Plane**:
   - `kube-apiserver`: Pusat komunikasi REST dan gerbang validasi state cluster.
   - `etcd`: Penyimpanan key-value terdistribusi yang konsisten dan berkonsensus Raft.
   - `kube-scheduler`: Memilih node pekerja terbaik berdasarkan resource requests/limits, tolerations, dan affinity rules.
   - `kube-controller-manager`: Menjalankan loop rekonsiliasi (*control loop*) untuk mencapai status aktual yang sesuai dengan *desired state*.
2. **Worker Node**:
   - `kubelet`: Agen pekerja yang berkomunikasi dengan container runtime via Container Runtime Interface (CRI).
   - `kube-proxy`: Mengelola aturan forwarding paket IP (iptables / IPVS) untuk abstraksi Kubernetes Service.

## 3. Anatomi Teknis & Cara Kerja Internal
Loop Rekonsiliasi Inti Kubernetes: `for { actual_state = observe(); if actual_state != desired_state { reconcile(actual_state, desired_state) } }`. Jika sebuah container crash, kubelet mendeteksinya melalui liveness probe dan secara otomatis merestart container.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```yaml
# Manifes Kubernetes Produksi: Deployment dengan Rolling Update & Resource Constraints
apiVersion: apps/v1
kind: Deployment
metadata:
  name: high-availability-api
  labels:
    app: api-server
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
      - name: api-container
        image: my-registry/api-server:v1.2.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

## 5. Miskonsepsi & Jebakan Industri
Tidak mendefinisikan Resource Requests dan Limits: pod yang mengalami kebocoran memori (memory leak) dapat memakan seluruh RAM pada worker node hingga memicu kernel Linux OOM Killer untuk mematikan proses sistem kritis node tersebut.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
Level 1: Tulis manifes Kubernetes Service dan Ingress untuk mengekspos aplikasi web ke internet publik. Level 2: Bangun Custom Resource Definition (CRD) dan Kubernetes Operator sederhana menggunakan Python (Kopf) atau Go. Level 3: Rancang konfigurasi Istio Service Mesh untuk menerapkan mutual TLS (mTLS) dan circuit breaking antar pod.

## 7. Rekomendasi Sumber Belajar Standar Emas
- Burns, B., Beda, J., & Hightower, K. (2019). *Kubernetes: Up and Running (2nd ed.)*. O'Reilly Media.
- Beyer, B., Jones, C., Petoff, J., & Murphy, N. R. (2016). *Site Reliability Engineering*. O'Reilly Media.

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [154. devops-cloud-infrastructure-platform-engineering](./154-devops-cloud-infrastructure-platform-engineering.md) | *Berikutnya*: [156. observabilitas-tiga-pilar-sre](./156-observabilitas-tiga-pilar-sre.md)
