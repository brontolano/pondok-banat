path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

print("Total lines:", len(lines))
print("Line 4 length:", len(lines[3]))
print("Line 4:", repr(lines[3]))

# Read line 4 and do targeted replacements
line4 = lines[3]

# Replace Rev. 350 -> Rev. 351 (first occurrence only is fine, but let's check)
print("Rev. 350 count in line4:", line4.count('Rev. 350'))

new_line4 = line4
new_line4 = new_line4.replace('Rev. 350', 'Rev. 351', 1)
new_line4 = new_line4.replace('bb78199', 'e02e207')
new_line4 = new_line4.replace('10 commits ahead', '12 commits ahead')

print("New line 4:", repr(new_line4))

# Verify the replacement is correct
assert new_line4 != line4, "No replacement made!"
assert 'Rev. 351' in new_line4
assert 'e02e207' in new_line4
assert '12 commits ahead' in new_line4

lines[3] = new_line4

with open(path, 'w') as f:
    f.writelines(lines)

print("Header updated.")
