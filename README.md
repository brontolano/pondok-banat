# Pondok Banat MVP

**Platform Manajemen Pesantren Putri** — Administrasi, Kurikulum, Akademik & Komunikasi.

## Features
- Role-based login: Admin, Guru, Wali Kelas, Pengasuh/Staff
- Santri data read-only (sementara)
- SQLite database with 15 tables
- Simple, mobile-first UI/UX

## Prerequisites
- Node.js 18+
- npm

## Installation
```bash
npm install
npm run dev
```

## Build
```bash
npm run build
npm start
```

## Database
SQLite file: `dev.db` (15 tables: users, roles, students, classes, teachers, subjects, silabus, rpp, grades, absensi, rapor, announcements, messages, notifications)

## Project Structure
```
src/
  app/          # Next.js pages (12)
  components/   # React components
  lib/          # Database & utilities
prisma/         # PRISMA schema (optional)
