import sqlite3, uuid
from datetime import datetime

DB = '/opt/data/home/workspace/dev/pondok-banat/dev.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# 1. Add Takhosous class (was skipped by import_excel.py bug)
c.execute("SELECT COUNT(*) FROM classes WHERE kode = 'Takhosous'")
if c.fetchone()[0] == 0:
    cid = str(uuid.uuid4())
    c.execute("INSERT INTO classes (id, kode, nama, seksi, jenjang, program, wali_kelas_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (cid, 'Takhosous', 'Takhosous', None, 'Takhosous', None, None, datetime.now().isoformat(), datetime.now().isoformat()))
    print('Added Takhosous class:', cid)
else:
    print('Takhosous already exists')
conn.commit()

# 2. Seed users and roles (M01)
c.execute("SELECT COUNT(*) FROM roles")
if c.fetchone()[0] == 0:
    now = datetime.now().isoformat()
    # Roles
    roles = [
        ('admin', 'admin', 'Administrator', 'Seluruh modul', now),
        ('guru', 'guru', 'Guru', 'Input nilai, absensi, lihat silabus & RPP', now),
        ('wali_kelas', 'wali_kelas', 'Wali Kelas', 'Kelas & akademik: nilai, absensi, kegiatan, presensi', now),
        ('pengasuh', 'pengasuh', 'Pengasuh/Staff', 'Lihat data anak (nilai, absensi, kegiatan) — read-only', now),
        ('santri', 'santri', 'Santri', 'Informasi pribadi (data tampilan) — read-only', now),
    ]
    for r in roles:
        cid = str(uuid.uuid4())
        c.execute("INSERT INTO roles (id, name, display_name, description, permissions) VALUES (?, ?, ?, ?, ?)",
                  (cid, r[0], r[1], r[2], r[3]))
    conn.commit()
    print('Roles seeded:', len(roles))

    # Admin user
    uid = str(uuid.uuid4())
    c.execute("INSERT INTO users (id, email, password, name, role, status, kelas_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (uid, 'admin@pondokanat.com', 'admin123', 'Admin Pondok Banat', 'admin', 'active', None, now, now))
    conn.commit()
    print('Admin user seeded')

    # Seed role_permissions (M01 all permissions)
    perms = [
        ('admin', 'M01:read'), ('admin', 'M01:write'), ('admin', 'M01:export'), ('admin', 'M01:admin'),
        ('guru', 'M03:read'), ('guru', 'M03:write'), ('guru', 'M03:export'),
        ('guru', 'M04:read'), ('guru', 'M04:write'), ('guru', 'M04:export'),
        ('guru', 'M05:read'), ('guru', 'M05:write'), ('guru', 'M05:export'),
        ('guru', 'M08:read'), ('guru', 'M08:write'), ('guru', 'M08:export'),
        ('wali_kelas', 'M02:read'), ('wali_kelas', 'M02:write'),
        ('wali_kelas', 'M03:read'), ('wali_kelas', 'M03:write'),
        ('wali_kelas', 'M04:read'), ('wali_kelas', 'M04:write'),
        ('wali_kelas', 'M05:read'), ('wali_kelas', 'M05:write'),
        ('wali_kelas', 'M07:read'), ('wali_kelas', 'M07:write'),
        ('wali_kelas', 'M08:read'), ('wali_kelas', 'M08:write'),
        ('pengasuh', 'M05:read'), ('pengasuh', 'M08:read'),
        ('santri', 'M05:read'), ('santri', 'M06:read'), ('santri', 'M08:read'),
    ]
    for rp in perms:
        cid = str(uuid.uuid4())
        c.execute("INSERT INTO role_permissions (id, role_id, permission) VALUES (?, ?, ?)",
                  (cid, rp[0], rp[1]))
    conn.commit()
    print('Role permissions seeded:', len(perms))
else:
    print('Roles already exist:', c.fetchone()[0])

conn.close()
print('DONE')
