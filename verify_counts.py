import sqlite3
con = sqlite3.connect('dev.db')
print('grades rows:', con.execute('SELECT COUNT(*) FROM grades').fetchone()[0])
print('mapel count:', con.execute('SELECT COUNT(*) FROM subjects').fetchone()[0])
print('siswa inactive:', con.execute("SELECT COUNT(*) FROM students WHERE status='inactive'").fetchone()[0])
print('siswa active:', con.execute("SELECT COUNT(*) FROM students WHERE status='active'").fetchone()[0])
print('classes:', con.execute('SELECT COUNT(*) FROM classes').fetchone()[0])
