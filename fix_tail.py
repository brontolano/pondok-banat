with open('PRD-PONDOK-BANAT.md', 'r') as f:
    content = f.read()

# Find the corrupted line and fix it
corrupted = "> - **Commit count:** 906 / 13/0 (fresh verification > - **Commit count:** 905 / 12/0 (fresh verification & stability confirmation, 03 November 2026 WIB); HEAD `c7cad53` (Rev. 858 committed — PRD synced ke Rev. 858); **905 / 12/0** (905 local commits, 12 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 857 (data terkonsisten). stability confirmation, 03 November 2026 WIB); HEAD `dd95607` (Rev. 858 committed — PRD synced ke Rev. 858); **906 / 13/0** (906 local commits, 13 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 857 (data terkonsisten)."

fixed = "> - **Commit count:** 906 / 13/0 (fresh verification & stability confirmation, 03 November 2026 WIB); HEAD `dd95607` (Rev. 858 committed — PRD synced ke Rev. 858); **906 / 13/0** (906 local commits, 13 ahead / 0 behind origin_main). State stabil, tidak ada perubahan signifikan dari Rev. 857 (data terkonsisten)."

if corrupted in content:
    content = content.replace(corrupted, fixed)
    with open('PRD-PONDOK-BANAT.md', 'w') as f:
        f.write(content)
    print("Fixed corrupted tail")
else:
    print("Corrupted pattern not found exactly")
