# Modul 155: Orkestrasi Kontainer: Bedah Internal Kubernetes (K8s Control Plane, Pods, Deployments, Services, Ingress, Istio)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [154. devops-cloud-infrastructure-platform-engineering](./154-devops-cloud-infrastructure-platform-engineering.md) | *Berikutnya*: [156. observabilitas-tiga-pilar-sre](./156-observabilitas-tiga-pilar-sre.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Di masa lalu, mengonfigurasi infrastruktur cloud—membuat puluhan server virtual, load balancer, aturan firewall, dan database terkelola di Amazon Web Services (AWS) atau Google Cloud Platform (GCP)—dilakukan dengan cara mengklik tombol-tombol di halaman web konsol browser (*ClickOps*). Satu klik yang salah pada aturan firewall dapat membuka database ke seluruh hacker dunia tanpa ada jejak siapa yang mengubahnya! Infrastructure as Code (IaC) & Cloud Native ([Terraform & Infrastructure as Code](https://developer.hashicorp.com/terraform/intro)) adalah revolusi kedisiplinan rekayasa: Anda menuliskan seluruh arsitektur data center Anda dalam file teks deklaratif (Terraform HCL). Infrastruktur Anda dapat disimpan di Git, ditinjau melalui Pull Request oleh rekan tim (*Peer Review*), diuji secara otomatis, dan dibangun kembali dari nol di belahan dunia lain dalam hitungan menit hanya dengan mengetik perintah sakti: `terraform apply`.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Prinsip Pendekatan Deklaratif vs Imperatif dan Graf Ketergantungan Topologi Terraform:

1. **Deklaratif (Terraform, OpenTofu, CloudFormation)**:
   Anda mendeklarasikan *APA* hasil akhir yang Anda inginkan (misal: *'Tersedia 1 VPC dengan 3 Subnet Publik'*).    Engine IaC menghitung sendiri urutan langkah kerja yang dibutuhkan untuk mencapai status tersebut.
   - **Idempoten (Idempotency)**: Menjalankan `terraform apply` sepuluh kali berturut-turut pada infrastruktur yang sudah ada menghasilkan perubahan **0 resource**.

2. **Imperatif (Ansible, Bash Scripts, Chef)**:
   Anda mendikte langkah demi langkah *BAGAIMANA* cara membangunnya (misal: *'Jalankan perintah apt-get install, lalu copy file'*).

3. **Siklus Hidup dan File State Terraform (`terraform.tfstate`)**:
   File state adalah peta penghubung antara kode deklaratif Anda dengan ID sumber daya fisik di cloud vendor:
   $$\text{Resource In Code: } \texttt{aws\_s3\_bucket.b} \xleftrightarrow{\text{State Map}} \text{Cloud Asset: } \texttt{"arn:aws:s3:::my-company-prod-bucket"}$$
   - **Directed Acyclic Graph (DAG) Execution**: Terraform memetakan seluruh ketergantungan sumber daya ke dalam pohon DAG dan mengeksekusi pembuatan sumber daya independen secara paralel bersamaan.

## 3. Anatomi Teknis & Cara Kerja Internal
Alur Kerja Tiga Langkah Eksekusi Terraform Core Engine:

```mermaid
graph LR
A[Declarative Code .tf] --> B[terraform init: Download Provider Plugins AWS/GCP]
B --> C[terraform plan: Compare Code vs State vs Real Cloud Reality]
C --> D{Plan Spec: Shows Exact Changes (+Add, ~Change, -Destroy)}
D -->|User Approves| E[terraform apply: Parallel Provisioning via Cloud APIs]
E --> F[Update Remote State Lock S3/DynamoDB Backend]
end
```

1. **State Locking (DynamoDB / GCS / Terraform Cloud)**:
   Mencegah dua insinyur perangkat lunak mengeksekusi `terraform apply` di saat yang sama. Engine mengunci file state (*State Lock*) saat operasi plan/apply dimulai dan melepasnya setelah proses selesai.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```hcl
# Production-Ready Terraform HCL Manifest Provisioning Secure AWS S3 Bucket
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "secure_telemetry_storage" {
  bucket        = "company-secure-telemetry-prod-bucket-2026"
  force_destroy = false

  tags = {
    Environment = "Production"
    ManagedBy   = "Terraform-IaC"
  }
}

# Kunci seluruh akses publik untuk mencegah kebocoran data rahasia!
resource "aws_s3_bucket_public_access_block" "block_public" {
  bucket = aws_s3_bucket.secure_telemetry_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

## 5. Miskonsepsi & Jebakan Industri
1. **Configuration Drift via Out-of-Band Console Modifications**: Administrator memodifikasi aturan security group firewall secara manual via web konsol cloud AWS tanpa memperbarui kode Terraform. Saat insinyur lain menjalankan `terraform apply`, Terraform akan mendeteksi perbedaan dan menghapus perubahan manual tersebut secara otomatis (*Drift Overwrite*).
2. **Exposing Unencrypted Secrets in `terraform.tfstate`**: Mendefinisikan kata sandi database secara plaintext di kode Terraform. File `terraform.tfstate` menyimpan seluruh nilai rahasia dalam format JSON mentah tanpa enkripsi default jika backend state lokal tidak diamankan.
3. **Accidental Disaster Destruction via Resource Renaming**: Mengubah nama pengenal sumber daya di kode (`resource "aws_db_instance" "db_old"` diubah menjadi `"db_new"`). Terraform menganggap Anda ingin **MENGHAPUS DATABASE LAMA** dan membuat database baru yang kosong melompong (solusi: gunakan blok `moved` di Terraform 1.1+).

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Tulis konfigurasi Terraform lokal menggunakan *Local Provider* (`hashicorp/local`) yang membuat file teks `inventory.txt` di disk lokal Anda. Eksekusi `terraform init`, `terraform plan`, dan `terraform apply`.
2. **Tingkat Menengah**: Gunakan emulator cloud open-source LocalStack untuk mem-provisioning VPC, Subnet, dan instance VM EC2 virtual menggunakan Terraform tanpa perlu membayar akun AWS nyata.
3. **Tingkat Mahir**: Rancang modul Terraform reusable yang menerapkan arsitektur Multi-Tier High Availability (VPC multi-AZ, Private/Public Subnets, NAT Gateways, dan Auto-Scaling Group). Konfigurasikan Remote State Backend dengan enkripsi S3 dan mekanisme State Locking menggunakan tabel DynamoDB.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Terraform: Up & Running, 3rd Edition | Yevgeniy Brikman (Gruntwork) | [O'Reilly Terraform Book](https://www.terraformupandrunning.com/) | Alkitab Terraform: Modules, State Management, Loops & Zero-Downtime Deployment |
| Infrastructure as Code: Dynamic Systems for the Cloud Era | Kief Morris (ThoughtWorks) | [O'Reilly IaC Book](https://www.oreilly.com/library/view/infrastructure-as-code/9781098114671/) | Prinsip Dasar IaC, Immutability, Antifragile Platforms & Pipelines |
| HashiCorp Terraform Documentation | HashiCorp / OpenTofu | [Terraform Official Documentation](https://developer.hashicorp.com/terraform/docs) | Bahasa HCL, Provider Architecture, CLI Commands & State Backends |
| OpenTofu: Open Source Alternative to Terraform | Linux Foundation | [OpenTofu Official Portal](https://opentofu.org/) | Fork Komunitas Bebas Open-Source untuk Manajemen Infrastruktur Cloud Native |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [154. devops-cloud-infrastructure-platform-engineering](./154-devops-cloud-infrastructure-platform-engineering.md) | *Berikutnya*: [156. observabilitas-tiga-pilar-sre](./156-observabilitas-tiga-pilar-sre.md)
