with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# The correct structure should end with the Rev. 170 section (line 3563) + --- + final Rev. 171 section
# We need to find the clean cutoff point: after the Rev. 170 section's closing ---
# and keep only one final Rev. 171 section at the very end

# Find the last occurrence of the clean separator before the final section
# The clean file should have the Rev. 170 section ending at line 3587 (---), then the final Rev. 171 section

# Let's find the last "---" before the final section
content_str = open('PRD-PONDOK-BANAT.md', 'r').read()

# Find the last occurrence of "---" before the final "## 58. REVISI TERBARU (Rev. 171"
# The clean file ends with the Rev. 170 section (ending at line 3587 with ---), then the final section

# Strategy: Find the last occurrence of "## 57. REVISI TERBARU (Rev. 170" and keep everything up to its closing ---
# Then append the final "## 58. REVISI TERBARU (Rev. 171..." section

import re

with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Find the Rev. 170 section start
rev170_start = content.rfind('## 57. REVISI TERBARU (Rev. 170')
if rev170_start == -1:
    print("Rev. 170 section not found!")
else:
    print(f"Rev. 170 section starts at index {rev170_start}")
    
    # Find the closing --- after the Rev. 170 section
    rev170_end = content.find('\n---\n', rev170_start)
    if rev170_end == -1:
        print("Closing --- not found!")
    else:
        print(f"Rev. 170 section ends at index {rev170_end}")
        
        # Find the final Rev. 171 section (the one at the very end)
        final_section_start = content.rfind('## 58. REVISI TERBARU (Rev. 171')
        if final_section_start == -1:
            print("Final Rev. 171 section not found!")
        else:
            print(f"Final Rev. 171 section starts at index {final_section_start}")
            
            # Clean content: everything up to the closing --- of Rev. 170, plus the final section
            clean_content = content[:rev170_end + 4] + content[final_section_start:]
            
            with open('PRD-PONDOK-BANAT.md', 'w') as f:
                f.write(clean_content)
            
            print(f"Original length: {len(content)}")
            print(f"Clean length: {len(clean_content)}")
            print("Done")