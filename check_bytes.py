import sys
path = '/opt/data/home/workspace/dev/pondok-banat/update_prd_rev20.py'
with open(path, 'rb') as f:
    data = f.read()
# Find the pattern line
idx = data.find(b'pattern = r')
print('Found at:', idx)
# Show the line
line_end = data.find(b'\n', idx)
line = data[idx:line_end]
print('Line bytes:')
print(repr(line))
print()
# Count backslashes in the pattern part
# The pattern is r'> \*\*Rev\. 19.*?<pattern_part>Perbaikan:...'
# Find the <pattern_part>
start = line.find(b'> ')
end = line.find(b'Perbaikan:')
pattern_part = line[start+len(b'> '):end]
print('Pattern part bytes:', repr(pattern_part))
print('Number of backslashes in pattern part:', pattern_part.count(b'\\'))
print('Number of asterisks in pattern part:', pattern_part.count(b'*'))
print()
# Check what the file should have
# Old: r'> \*\*Rev\. 19.*?\\*\\*Perbaikan:...'
# New: r'> \*\*Rev\. 19.*?\*\*Perbaikan:...'
print('Old pattern part (expected):', repr(b"> \\*\\*Rev\\. 19.*?\\\\*\\\\*Perbaikan:"))
print('New pattern part (expected):', repr(b"> \\*\\*Rev\\. 19.*?\\*\\*Perbaikan:"))
