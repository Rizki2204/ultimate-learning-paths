# Modul 156: Observabilitas Tiga Pilar & SRE (Structured Logging Loki, Prometheus PromQL, Grafana, OpenTelemetry, SLI/SLO)

**Navigasi**: [⬅️ Master Index](../../INDEX.md) | [Tingkat 9: Tingkat 9: Software Engineering, Front-End, Back-End, Full-Stack & Cloud/SRE](./README.md)
*Sebelumnya*: [155. orkestrasi-kontainer-bedah-internal-kubernetes](./155-orkestrasi-kontainer-bedah-internal-kubernetes.md) | *Berikutnya*: [157. fondasi-teoretis-basis-data-model-relasional](../10-basis-data-enterprise/157-fondasi-teoretis-basis-data-model-relasional.md)

---

## 1. Intuisi Dasar Tanpa Jargon ("Seperti Bayi Baru Lahir")
Ketika pesawat terbang modern mengangkasa di ketinggian 35.000 kaki, pilot di kokpit tidak perlu menoleh keluar jendela untuk menebak kondisi mesin; ratusan sensor telemetri menampilkan data tekanan oli, getaran turbin, dan kecepatan angin secara real-time pada layar instrumen. Observabilitas Sistem & Site Reliability Engineering (SRE) ([Google SRE & OpenTelemetry](https://sre.google/sre-book/table-of-contents/)) adalah kokpit instrumen bagi sistem perangkat lunak terdistribusi modern. Diciptakan oleh Ben Treynor Sloss di Google pada tahun 2003, filosofi SRE menyatakan: *'SRE adalah apa yang terjadi ketika Anda meminta seorang software engineer untuk merancang tim operasi sistem.'* Alih-alih menuntut 100% kesempurnaan yang mustahil secara ekonomi, SRE mendefinisikan batas kesalahan yang dapat diterima (**Error Budget**) melalui **SLO dan SLI**; mengumpulkan Tiga Pilar Observabilitas (**Metrics, Logs, Traces**) menggunakan standar universal **OpenTelemetry**; dan secara sengaja menyuntikkan kegagalan ke dalam sistem produksi (**Chaos Engineering**) untuk membuktikan keandalan sistem sebelum badai nyata menerjang.

## 2. Fondasi Teoretis & Aksiomatik / Matematis
Formulasi Matematis Metrik Keandalan SRE (SLI, SLO, SLA & Error Budgets):

1. **Indikator Tingkat Layanan (Service Level Indicator / SLI)**:
   Ukuran kuantitatif riil kepatuhan layanan yang diamati secara langsung:
   $$\text{SLI} = \frac{\text{Jumlah Peristiwa Baik (Kueri Sukses < 200ms)}}{\text{Jumlah Total Peristiwa Valid}} \times 100\%$$

2. **Tujuan Tingkat Layanan (Service Level Objective / SLO)**:
   Target keandalan internal yang disepakati bersama antara tim bisnis dan tim engineering (misal: $\text{SLO} = 99.9\%$ kueri sukses per bulan).

3. **Perjanjian Tingkat Layanan (Service Level Agreement / SLA)**:
   Janji kontrak hukum kepada pelanggan luar yang disertai konsekuensi denda penalti finansial (biasanya dipatok lebih longgar dari SLO, misal $99.5\%$).

4. **Anggaran Kesalahan (Error Budget)**:
   Ruang inovasi untuk melakukan rilis fitur baru dan eksperimen sistem:
   $$\text{Error Budget} = 100\% - \text{SLO}$$
   Untuk target SLO $99.9\%$ dalam satu bulan (43.200 menit):
   $$\text{Jatah Downtime yang Diizinkan} = 0.1\% \times 43.200\text{ menit} = \mathbf{43.2\text{ Menit / Bulan}}$$
   Jika Error Budget habis terbakar di awal bulan, seluruh rilis fitur baru dibekukan; tim diwajibkan 100% fokus memperbaiki stabilitas sistem!

## 3. Anatomi Teknis & Cara Kerja Internal
Tiga Pilar Observabilitas Terdistribusi dan Standar Arsitektur OpenTelemetry (OTel):

```mermaid
graph TD
subgraph Three Pillars of Observability
A[Metrics: Agregat Angka Numerik Waktu Deret Time-Series Prometheus] 
B[Logs: Catatan Teks Peristiwa Terstruktur JSON Fluentd/Elasticsearch]
C[Traces: Rekaman Perjalanan Menembus Batas Microservice OpenTelemetry/Jaeger]
end
subgraph Distributed Tracing Span Context
D[Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736 (Global Unique)] --> E[Span ID Parent: Root HTTP Request]
E --> F[Span ID Child 1: Auth Service Validation]
E --> G[Span ID Child 2: SQL Database Query: 45ms]
end
```

1. **W3C Trace Context Standard**: Menyisipkan header standar `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01` pada setiap pemanggilan HTTP dan gRPC melintasi jaringan, memungkinkan visualisasi perjalanan satu request melintasi 50 microservices terpisah.

## 4. Implementasi Praktis & Kode / Simulasi Riil
```python
# Prometheus Metrics Instrumentation in Python API Application
import time
from prometheus_client import Counter, Histogram, start_http_server

# 1. Counter Metric: Menghitung total request masuk
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests processed', 
    ['method', 'endpoint', 'http_status']
)

# 2. Histogram Metric: Mengukur latensi waktu respon dalam bucket detik
REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 
    'HTTP request latency in seconds',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)

def handle_web_request(endpoint: str):
    start_time = time.time()
    status = "200"
    try:
        # Simulasikan komputasi logika bisnis
        time.sleep(0.04)
    except Exception:
        status = "500"
    finally:
        duration = time.time() - start_time
        REQUEST_COUNT.labels(method="GET", endpoint=endpoint, http_status=status).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)

print("Prometheus instrumentation metrics ready!")
```

## 5. Miskonsepsi & Jebakan Industri
1. **High Cardinality Metrics Explosion in Prometheus**: Menyisipkan ID unik yang berubah-ubah (seperti `user_id`, nomor kartu kredit, atau UUID) sebagai label dimensi metrik Prometheus. Jutaan deret waktu (*Time Series*) unik akan tercipta, menghabiskan seluruh memori RAM server Prometheus dalam hitungan menit.
2. **Alert Fatigue Crisis**: Mengonfigurasi peringatan alarm pager pada kondisi non-kritis (seperti 'Penggunaan CPU server mencapai 85%'). Tim on-call menerima 50 notifikasi di tengah malam dan mulai mengabaikan seluruh alarm, sehingga ketika insiden fatal nyata terjadi, tidak ada yang merespons.
3. **Blameless Post-Mortem Violation**: Mengadakan investigasi insiden pasca-bencana (*Post-Mortem*) yang berfokus mencari 'siapa insinyur yang bersalah' untuk dihukum, alih-alih memperbaiki sistem dan prosedur keamanan. Membunuh budaya transparansi dan membuat insinyur menyembunyikan kesalahan masa depan.

## 6. Proyek Latihan & Rubrik Penilaian Mandiri
1. **Tingkat Pemula**: Hitung sisa Error Budget (dalam hitungan menit downtime yang tersisa) jika layanan dengan SLO bulanan 99.95% mengalami insiden pemadaman selama 15 menit pada minggu pertama bulan tersebut.
2. **Tingkat Menengah**: Pasang server Prometheus lokal dan ekspor metrik dari skrip Python di atas. Tulis kueri PromQL untuk menghitung laju permintaan per detik (`rate(http_requests_total[5m])`) dan persentil latensi ke-95 (`histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`.
3. **Tingkat Mahir**: Rancang eksperimen Chaos Engineering menggunakan alat Chaos Mesh atau LitmusChaos di klaster Kubernetes: suntikkan latensi jaringan buatan 300 ms dan packet loss 10% pada pod database, lalu amati apakah Circuit Breaker aplikasi klien berhasil membuka proteksi fail-fast tanpa merusak pengalaman pengguna.

## 7. Rekomendasi Sumber Belajar Standar Emas
| Sumber Pembelajaran | Penulis / Institusi | Tautan Langsung | Fokus Materi |
| :--- | :--- | :--- | :--- |
| Site Reliability Engineering: How Google Runs Production Systems | Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Murphy (Google) | [Google SRE Book Free](https://sre.google/sre-book/table-of-contents/) | Alkitab Resmi SRE: Service Level Objectives, Error Budgets, On-Call & Postmortems |
| OpenTelemetry: Cloud-Native Observability Standards | CNCF OpenTelemetry Project | [OpenTelemetry Official Portal](https://opentelemetry.io/) | Standar Industri Terpadu Traces, Metrics, Logs & OTLP Protocol |
| Prometheus: Up & Running (Infrastructure & Application Monitoring) | Brian Brazil (Prometheus Core Developer) | [O'Reilly Prometheus](https://www.oreilly.com/library/view/prometheus-up/9781492034131/) | PromQL Architecture, Metric Types (Counter/Gauge/Histogram) & Alerting Rules |
| Chaos Engineering: System Resiliency in Practice | Casey Rosenthal & Nora Jones (Netflix) | [O'Reilly Chaos Engineering](https://www.oreilly.com/library/view/chaos-engineering/9781492043850/) | Prinsip Eksperimen Kegagalan Terencana, Chaos Monkey & Blast Radius Control |

---
*Navigasi Cepat*: [Ke Tingkat 9](./README.md) | [Ke Master Index](../../INDEX.md) | *Sebelumnya*: [155. orkestrasi-kontainer-bedah-internal-kubernetes](./155-orkestrasi-kontainer-bedah-internal-kubernetes.md) | *Berikutnya*: [157. fondasi-teoretis-basis-data-model-relasional](../10-basis-data-enterprise/157-fondasi-teoretis-basis-data-model-relasional.md)
