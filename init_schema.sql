-- MVP Schema (SQLite)
-- Tables: users, roles, role_permissions, students, classes, teachers, subjects, silabus, rpp, absensi, grades, rapor, announcements, messages, notifications

-- 1. Users & Roles (M01)
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password TEXT,
    name TEXT,
    role TEXT CHECK(role IN ('admin','guru','wali_kelas','pengasuh','santri')),
    status TEXT DEFAULT 'active' CHECK(status IN ('active','inactive')),
    kelas_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE,
    display_name TEXT,
    description TEXT,
    permissions TEXT
);

CREATE TABLE IF NOT EXISTS role_permissions (
    id TEXT PRIMARY KEY,
    role_id TEXT,
    permission TEXT,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- 2. Master Data Santri (M02)
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    nisn TEXT UNIQUE,
    name TEXT,
    jk TEXT,
    ttl TEXT,
    kelas_id TEXT,
    status TEXT DEFAULT 'active',
    no_hp TEXT,
    alamat TEXT,
    photo TEXT,
    uid_nfc TEXT, -- NFC card UID: 'AF:C2:99:E7'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kelas_id) REFERENCES classes(id)
);

CREATE TABLE IF NOT EXISTS classes (
    id TEXT PRIMARY KEY,
    kode TEXT UNIQUE,
    nama TEXT,
    seksi TEXT,
    jenjang TEXT,
    program TEXT,
    wali_kelas_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. Master Data Guru & Staf (M03)
CREATE TABLE IF NOT EXISTS teachers (
    id TEXT PRIMARY KEY,
    nip TEXT UNIQUE,
    name TEXT,
    jk TEXT,
    jabatan TEXT,
    status TEXT DEFAULT 'active',
    kelas_id TEXT,
    no_hp TEXT,
    email TEXT,
    alamat TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kelas_id) REFERENCES classes(id)
);

-- 4. Kurikulum & Kitab Kuning (M04)
CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,
    kode TEXT,
    name TEXT,
    jml_jp INTEGER,
    pengajar_id TEXT,
    kelas_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kelas_id) REFERENCES classes(id),
    FOREIGN KEY (pengajar_id) REFERENCES teachers(id)
);

CREATE TABLE IF NOT EXISTS silabus (
    id TEXT PRIMARY KEY,
    kelas_id TEXT,
    mapel_id TEXT,
    semester TEXT,
    bahan TEXT,
    materi TEXT,
    target TEXT,
    metode TEXT,
    tujuan TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kelas_id) REFERENCES classes(id),
    FOREIGN KEY (mapel_id) REFERENCES subjects(id)
);

CREATE TABLE IF NOT EXISTS rpp (
    id TEXT PRIMARY KEY,
    kelas_id TEXT,
    mapel_id TEXT,
    minggu INTEGER,
    topik TEXT,
    metode TEXT,
    sumber TEXT,
    file TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kelas_id) REFERENCES classes(id),
    FOREIGN KEY (mapel_id) REFERENCES subjects(id)
);

-- 5. Akademik & Absensi (M05)
CREATE TABLE IF NOT EXISTS absensi (
    id TEXT PRIMARY KEY,
    student_id TEXT,
    kelas_id TEXT,
    tanggal DATETIME,
    jam TEXT,
    kegiatan TEXT,
    status TEXT DEFAULT 'H',
    created_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (kelas_id) REFERENCES classes(id)
);

CREATE TABLE IF NOT EXISTS grades (
    id TEXT PRIMARY KEY,
    student_id TEXT,
    kelas_id TEXT,
    mapel_id TEXT,
    semester TEXT,
    minggu INTEGER,
    mei REAL,
    smt REAL,
    absen REAL,
    hasil REAL DEFAULT 0,
    note TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (kelas_id) REFERENCES classes(id),
    FOREIGN KEY (mapel_id) REFERENCES subjects(id)
);

CREATE TABLE IF NOT EXISTS rapor (
    id TEXT PRIMARY KEY,
    student_id TEXT,
    kelas_id TEXT,
    semester TEXT,
    tahun TEXT,
    nilai TEXT,
    keterangan TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (kelas_id) REFERENCES classes(id)
);

-- 8. Communication & Notification (M08)
CREATE TABLE IF NOT EXISTS announcements (
    id TEXT PRIMARY KEY,
    title TEXT,
    body TEXT,
    kelas_id TEXT,
    created_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kelas_id) REFERENCES classes(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    sender_id TEXT,
    receiver_id TEXT,
    type TEXT,
    title TEXT,
    body TEXT,
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    type TEXT,
    title TEXT,
    body TEXT,
    is_read BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_students_kelas ON students(kelas_id);
CREATE INDEX IF NOT EXISTS idx_students_nisn ON students(nisn);
CREATE INDEX IF NOT EXISTS idx_teachers_jabatan ON teachers(jabatan);
CREATE INDEX IF NOT EXISTS idx_teachers_kelas ON teachers(kelas_id);
CREATE INDEX IF NOT EXISTS idx_absensi_siswa ON absensi(student_id, tanggal);
CREATE INDEX IF NOT EXISTS idx_grade_siswa ON grades(student_id, semester);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_messages_receiver ON messages(receiver_id, is_read);
