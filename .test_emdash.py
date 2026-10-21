# Minimal test
today_str = "20 Oktober 2026"
head_commit = "93d755f00d9756ab07fc0b27dba539f6152501c6"
ahead = "22"

# Test 1: simple f-string with em dash
s1 = f"""## 12. REVISI TERBARU (Rev. 388 — {today_str} WIB)"""
print("Test 1 OK:", repr(s1))

# Test 2: f-string with em dash and placeholders
s2 = f"""\n> **Verifikasi fresh dilakukan:** {today_str} (WIB, cron run) — query `sqlite3` ke `dev.db`"""
print("Test 2 OK:", repr(s2))
