with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Find the position of the first "Commit count: 906 / 13/0" in §12
import re
pattern = r'(> - \*\*Commit count:\*\* 906 / 13/0 \(fresh verification & stability confirmation, 03 November 2026 WIB\); HEAD `dd95607` \(Rev\. 858 committed — PRD synced ke Rev\. 858\); \*\*906 / 13/0\*\* \(906 local commits, 13 ahead / 0 behind origin_main\)\. State stabil, tidak ada perubahan signifikan dari Rev\. 857 \(data terkonsisten\)\.)'

matches = list(re.finditer(pattern, content))
if matches:
    # Find the second occurrence (the duplicated one at the end)
    if len(matches) >= 2:
        # Keep everything up to the end of the first match
        end_pos = matches[0].end()
        new_content = content[:end_pos]
        
        with open('PRD-PONDOK-BANAT.md', 'w') as f:
            f.write(new_content)
        
        print("File fixed - removed duplicate tail")
    else:
        print(f"Only {len(matches)} match found, no duplicate to remove")
else:
    print("No matches found")
