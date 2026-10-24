with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", "r", encoding="utf-8") as f:
    content = f.read()

# Update main header (line 4)
old_header = """Rev. 519: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 519 (updated from Rev. 518), §11 kompakt changelog 116–520, §12 updated; HEAD `0cb6019d39efdcf87346274f5ede6e5b55b714b5` (Rev. 518 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); 1 / 0 (1 commit ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `0cb6019d39efdcf87346274f5ede6e5b55b714b5` (Rev. 518 commit, fresh verification dilakukan hari ini); **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync). Local branch **1 commit ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 519 (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."""

new_header = """Rev. 520: PRD fresh verification & stability confirmation (24 Oct 2026 WIB); header Rev. 520 (updated from Rev. 519), §11 kompakt changelog 116–520, §12 updated; HEAD `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit: PRD fresh verification & stability confirmation (24 Oct 2026 WIB)); 2 / 0 (2 commit ahead origin_main). Branch `main`, remote `brontolano/pondok-banat`. `git rev-parse HEAD` = `ea1ac69d39efdcf87346274f5ede6e5b55b714b5` (Rev. 519 commit, fresh verification dilakukan hari ini); **origin/main:** `d36eb62911dc50d7d2e452ac1d37a801024dd3b6` (Rev. 517, in sync). Local branch **2 commit ahead / 0 behind** origin_main. Working tree: `PRD-PONDOK-BANAT.md` cocak dengan HEAD (revisi terbaru = Rev. 520 (fresh verification), fresh verification dilakukan hari ini); seluruh file lain cocak dengan HEAD; untracked: 67 skrip utility (tidak terpantau dalam git); `commit_msg.txt` dihapus (build artifact); `git ls-files` = 187 file."""

if old_header in content:
    content = content.replace(old_header, new_header)
    print("Main header updated.")
else:
    print("Main header not found!")
    import re
    m = re.search(r"Rev\. \d+:", content)
    if m:
        print("Found Rev. pattern:", repr(content[m.start():m.start()+150]))

with open("/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Main header updated in file:", "Rev. 520: PRD fresh verification" in content)
