# TODOLIST — Aplikasi Pondok Banat (MVP)

> Central checklist: one ⏳ item per cycle. Update after each cycle.

## M01: Admin & User Management
- [x] Role & permission engine (roles table, role_permissions)
- [x] Login/authentication (login page, hardcoded auth)
- [ ] User CRUD (future iteration)

## M02: Master Data Santri
- [x] SQLite schema + seed data (students, classes)
- [x] Dashboard: class selector, student list, status badge
- [ ] Input/import student (future iteration)

## M03: Master Data Guru & Staf
- [x] Schema + seed (teachers, positions)
- [x] Dashboard: teacher list, jabatan filter
- [x] Import batch dari Excel (`import_excel.py` → 54 guru dari `DATA PARA PENGAJAR BANAT.xlsx`)

## M04: Kurikulum & Kitab Kuning
- [x] Schema + dashboard: syllabus, subjects, RPP
- [ ] Active learning plan (future iteration)

## M05: Akademik & Absensi
- [x] Schema + dashboard: gradebook, MEI/SMT/ABSEN/HASIL formula
- [ ] Input nilai (future iteration)

## M06: Hifz/Quran Memorization
- [ ] (inactive in MVP — Hifz module inactive)

## M07: Kesiswaan & Tunggangan
- [x] Schema + dashboard: facilities, activities
- [ ] Dormitory management (future iteration)

## M08: Komunikasi & Notifikasi
- [x] Schema + dashboard: announcements, news, berita
- [ ] Wali Santri portal (future iteration)

## M09: Laporan & Analytics
- [x] Dashboard: reports, PDF export buttons
- [ ] PDF generation (future iteration)

## M10: Payment/Keuangan
- [ ] (inactive in MVP)

## M11: Mobile & Offline
- [ ] (Gatsby mobile app — not in MVP)

## Architecture
- [x] Next.js 16 + React 19 + TypeScript
- [x] SQLite database (15 tables)
- [x] Simple, mobile-first UI/UX
- [x] Role-based navigation (4 roles + Santri read-only)
- [ ] CI/CD pipeline (future iteration)

## Open / Backlog
- [ ] Online mode (API routes)
- [ ] Password hashing (bcrypt)
- [ ] Export/backup/restore (Excel, PDF)
- [ ] Testing (unit + integration)
- [ ] Production deployment (Vercel, Docker)
