# Repo polish checklist & improvements (final)

Tujuan: membuat repository rapi, konsisten, dan mudah diikuti sebagai "master learning system".

1) Navigasi & struktur
- [ ] Pastikan README utama menjelaskan tujuan singkat dan navigasi langsung ke docs/index.md
- [ ] docs/index.md harus memetakan semua doc penting (sudah ada) dan validasi semua link
- [ ] Tambahkan /domains/ README yang ringkas menjelaskan setiap domain file

2) File & nama
- [ ] Gunakan penamaan konsisten: kebanyakan file di `docs/` dan `domains/` dengan huruf kecil dan tanda hubung
- [ ] Tambahkan header metadata singkat di setiap docs (Judul, ringkasan 1-2 baris, last-updated)

3) Cross-links & templates
- [ ] Setiap domain file tambahkan "Study plan (0–6 / 6–12 / 12–24 months)" dan "Project ideas"
- [ ] Tambahkan template file: docs/templates/domain-template.md dan docs/templates/project-template.md

4) Contribution & governance
- [ ] Tambahkan CONTRIBUTING.md dengan guidelines: issue templates, PR templates, commit message style
- [ ] Tambahkan CODE_OF_CONDUCT.md dan LICENSE (MIT atau sesuai pilihan)

5) Automation & CI
- [ ] Tambahkan basic GitHub Actions workflow that lints Markdown and checks dead links (/.github/workflows/markdown.yml)
- [ ] Add a preview step (optional) using GitHub Pages or mkdocs if desired

6) Project & portfolio integration
- [ ] Add a `projects/` directory with project templates and starter repos
- [ ] Add `examples/` with completed example project write-ups

7) Accessibility & readability
- [ ] Consistent headings and short paragraphs
- [ ] Add TOC for long docs (auto-generated via script or manually)

8) Final polish tasks I can run for you (pick any):
- [ ] Generate domain-template.md and project-template.md
- [ ] Add CONTRIBUTING.md and basic GitHub Actions workflow
- [ ] Validate and fix all internal links in docs/index.md and README.md
- [ ] Create projects/ with 3 example project write-ups

---

Jika setuju, saya akan langsung menambahkan: templates (domain + project), CONTRIBUTING.md, basic markdown lint workflow, dan memvalidasi link internal. Pilih kombinasi yang Anda ingin saya kerjakan sekarang.