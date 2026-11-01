#!/usr/bin/env python3
import os
os.chdir("/opt/data/home/workspace/dev/pondok-banat")

with open("PRD-PONDOK-BANAT.md", "r") as f:
    content = f.read()

# Fix header
content = content.replace("header Rev. 851 (tersimpan", "header Rev. 852 (tersimpan")
content = content.replace("§11 compact changelog 116–844→845→846→847→848→849→850→851", "§11 compact changelog 116–844→845→846→847→848→849→850→851→852")
content = content.replace("(Rev. 851 committed — PRD synced ke Rev. 851)", "(Rev. 852 committed — PRD synced ke Rev. 852)")
content = content.replace("Working tree: PRD synced ke Rev. 851", "Working tree: PRD synced ke Rev. 852")

# Fix §12 content
content = content.replace("(PRD ditulis ke Rev. 849)", "(PRD ditulis ke Rev. 852)")
content = content.replace("(Rev. 851 committed — PRD synced ke Rev. 851)", "(Rev. 852 committed — PRD synced ke Rev. 852)")
content = content.replace("**887 local commits, 1 ahead / 0 behind** origin_main", "**887 local commits, 2 ahead / 0 behind** origin_main")
content = content.replace("**887 / 1/0** (887 local commits, 1 ahead / 0 behind origin_main)", "**887 / 2/0** (887 local commits, 2 ahead / 0 behind origin_main)")

with open("PRD-PONDOK-BANAT.md", "w") as f:
    f.write(content)

print("Done")
