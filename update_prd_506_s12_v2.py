#!/usr/bin/env python3
"""Update §12 to Rev. 506."""

path = '/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md'

with open(path, 'r') as f:
    lines = f.readlines()

changed = False
for i, line in enumerate(lines):
    # §12 header: Rev. 468–505 -> Rev. 468–506
    if i == 432 and 'Rev. 468–505' in line:
        lines[i] = line.replace('Rev. 468–505', 'Rev. 468–506')
        print(f"§12 header updated at line {i+1}")
        changed = True

    # Verifikasi fresh kondisi repository: Rev. 503 -> Rev. 505
    if i == 435 and 'Rev. 503' in line:
        lines[i] = lines[i].replace('Rev. 503', 'Rev. 505')
        print(f"Verifikasi message updated at line {i+1}")
        changed = True

    # Git HEAD (local): bae146f4 -> dc9bd27f, Rev. 504 -> Rev. 506, 38 -> 40
    if i == 436:
        line = line.replace('bae146f4e9c2bc403bb5308ac64e0eee281419e7', 'dc9bd27f6be685f176bfed9c08be3674b17cf744')
        line = line.replace('(Rev. 504 (final): PRD fresh verification', '(Rev. 506 commit: PRD fresh verification')
        line = line.replace('header Rev. 504, §11 kompakt changelog 116–504, §12 updated', 'header Rev. 506, §11 kompakt changelog 116–506, §12 updated')
        line = line.replace('**38 commits ahead / 0 behind**', '**40 commits ahead / 0 behind**')
        lines[i] = line
        print(f"Git HEAD updated at line {i+1}")
        changed = True

    # Working tree: bae146f4 -> dc9bd27f, Rev. 504 -> Rev. 506
    if i == 437:
        line = line.replace('bae146f4e9c2bc403bb5308ac64e0eee281419e7', 'dc9bd27f6be685f176bfed9c08be3674b17cf744')
        line = line.replace('(revisi terbaru = Rev. 504 (final))', '(revisi terbaru = Rev. 506 (final))')
        line = line.replace('HEAD `bae146f4e9c2bc403bb5308ac64e0eee281419e7` (Rev. 504 (final))', 'HEAD `dc9bd27f6be685f176bfed9c08be3674b17cf744` (Rev. 506 commit)')
        lines[i] = line
        print(f"Working tree updated at line {i+1}")
        changed = True

    # Status: rev 504 (final) -> rev 506, bae146f4 -> dc9bd27f, 38 -> 40
    if i == 446:
        line = line.replace('(Rev. 504 (final)); 38 / 0 (38 commits ahead origin_main)', '(Rev. 506 commit); 40 / 0 (40 commits ahead origin_main)')
        line = line.replace('rev 504 (final)', 'rev 506')
        line = line.replace('bae146f4e9c2bc403bb5308ac64e0eee281419e7', 'dc9bd27f6be685f176bfed9c08be3674b17cf744')
        lines[i] = line
        print(f"Status updated at line {i+1}")
        changed = True

if not changed:
    print("No changes were made! Check the conditions.")

with open(path, 'w') as f:
    f.writelines(lines)

print("File saved")
