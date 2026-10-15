import sqlite3
conn = sqlite3.connect('dev.db')
cursor = conn.cursor()

# Count students
cursor.execute("SELECT COUNT(*) FROM students")
print(f"Students: {cursor.fetchone()[0]}")

# Count grades
cursor.execute("SELECT COUNT(*) FROM grades")
print(f"Grades: {cursor.fetchone()[0]}")

# Count classes
cursor.execute("SELECT COUNT(*) FROM classes")
print(f"Classes: {cursor.fetchone()[0]}")

# Count subjects
cursor.execute("SELECT COUNT(*) FROM subjects")
print(f"Subjects: {cursor.fetchone()[0]}")

# Students by class
cursor.execute("""
    SELECT c.kode, c.nama, COUNT(s.id) 
    FROM classes c 
    LEFT JOIN students s ON s.kelas_id = c.id 
    GROUP BY c.id, c.kode, c.nama
    ORDER BY c.kode
""")
print("\nStudents per class:")
for row in cursor.fetchall():
    print(f"  {row[0]} ({row[1]}): {row[2]}")

# Subjects
cursor.execute("SELECT name FROM subjects ORDER BY name")
print("\nSubjects:")
for row in cursor.fetchall():
    print(f"  {row[0]}")

conn.close()