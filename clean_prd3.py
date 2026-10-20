with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Find the Rev. 170 section start
rev170_start = content.rfind('## 57. REVISI TERBARU (Rev. 170')
if rev170_start == -1:
    print("Rev. 170 section not found!")
else:
    print(f"Rev. 170 section starts at index {rev170_start}")
    
    # Find the next "## " after Rev. 170 start (which would be the next section)
    next_section = content.find('\n## ', rev170_start + 1)
    if next_section == -1:
        print("No next section found!")
    else:
        print(f"Next section starts at index {next_section}")
        
        # The Rev. 170 section content is from rev170_start to next_section
        # We want to keep everything up to next_section, then the final Rev. 171 section
        
        # Find the final Rev. 171 section (the one at the very end)
        final_section_start = content.rfind('## 58. REVISI TERBARU (Rev. 171')
        if final_section_start == -1:
            print("Final Rev. 171 section not found!")
        else:
            print(f"Final Rev. 171 section starts at index {final_section_start}")
            
            # Clean content: everything up to next_section, plus the final section
            clean_content = content[:next_section] + content[final_section_start:]
            
            with open('PRD-PONDOK-BANAT.md', 'w') as f:
                f.write(clean_content)
            
            print(f"Original length: {len(content)}")
            print(f"Clean length: {len(clean_content)}")
            print("Done")