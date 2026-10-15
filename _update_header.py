import subprocess

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Update header (line 4): Rev. 41 -> Rev. 42, Rev. 40 -> Rev. 41, rev 41 -> rev 42
old_header = '> **Rev. 41 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 40 (data terverifikasi ulang).'
new_header = '> **Rev. 42 — 14 Oktober 2026 (WIB).** Verifikasi fresh kondisi repo + `dev.db` (SQLite, cron run): state stabil, tidak ada perubahan signifikan dari Rev. 41 (data terverifikasi ulang).'
content = content.replace(old_header, new_header)

# Update the end of the header: rev 41 -> rev 42
old_status = 'state stabil; rev 41 = verifikasi fresh & konfirmasi stabilitas.'
new_status = 'state stabil; rev 42 = verifikasi fresh & konfirmasi stabilitas.'
content = content.replace(old_status, new_status)

with open('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md', 'w') as f:
    f.write(content)

print('Done')
result = subprocess.run(['grep', '-n', 'Rev. 4[0-9]', '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'], capture_output=True, text=True)
print(result.stdout)
