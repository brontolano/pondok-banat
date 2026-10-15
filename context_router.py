#!/usr/bin/env python3
"""
context_router.py — peta konteks → agen dari agents/*.md

Digunakan agar setiap task otomatis menentukan agent mana yang harus dipanggil
(mengikuti Bab 10 PRD-PONDOK-BANAT.md). Baca folder agents/, cocokkan kata
kunci task, keluarkan daftar agen teratas + alasan.

Gunakan: python3 context_router.py "<task description>"
        atau: python3 context_router.py --list
"""

import os
import re
import sys
from pathlib import Path

AGENTS_DIR = Path('/opt/data/home/workspace/dev/pondok-banat/agents')
PRD_FILE = Path('/opt/data/home/workspace/dev/pondok-banat/PRD-PONDOK-BANAT.md')

# Kategori → pola kunci (regex). Daftar ini adalah "peta konteks" awal.
DEFAULT_CATEGORIES = {
    'code-reviewer': r'review|reviewer|code review|optimize|bug|fix|check|qa|correct',
    'software-architect': r'architecture|architect|design|scalab|structure|adr|detailed|system design',
    'backend-architect': r'backend|api|route|server|database|database|query|prisma|node|express|typescript',
    'frontend-developer': r'frontend|ui|ux|react|component|template|html|css|tailwind|view',
    'mobile-app-builder': r'mobile|android|ios|flutter|react native|app builder',
    'pdf-engine-architect': r'pdf|report|rapor|keluaran|export|laporan|cetak|print',
    'data-engineer': r'data|excel|xlsx|nilai|score|grade|database|etl|import|spreadsheet',
    'devops-automator': r'deploy|ci/cd|backup|host|server|infra|docker|environment|run|build|publish',
    'prompt-engineer': r'prompt|prompt engineering|instruction|agent|router',
    'privacy-engineer': r'privacy|security|password|token|secret|encrypt|authentication',
}


def load_agents():
    """Baca semua agent md, kembalikan list of dict {name, desc, path, content}."""
    agents = []
    if not AGENTS_DIR.is_dir():
        print(f"ERROR: {AGENTS_DIR} tidak ditemukan")
        return agents
    for f in sorted(AGENTS_DIR.glob('*.md')):
        content = f.read_text(encoding='utf-8', errors='replace')
        # Ambil name dari frontmatter
        name = f.stem.replace('engineering-', '').replace('-', ' ').title()
        desc = ''
        m = re.search(r'description:\s*\'?(.*?)\'?\s*$', content, re.MULTILINE)
        if m:
            desc = m.group(1)
        agents.append({
            'file': f.name,
            'name': name,
            'description': desc,
            'path': str(f),
            'content': content,
        })
    return agents


def match_agents(agents, task, top_n=5):
    """
    Cocokkan task dengan setiap agent.
    Peringkat: match spesifik (kata benda/versi tugas) di atas match generik.
    """
    task_lower = task.lower()
    # Kata kunci domain Pondok Banat (lebih spesifik dari "data")
    domain_kw = [
        'nilai', 'murid', 'santri', 'kelas', 'guru', 'admin', 'rapor',
        'absensi', 'kegiatan', 'kurikulum', 'arabi', 'islam', 'al-qur',
        'hadits', 'fiqih', 'tawhid', 'tjawid', 'konseling', 'penjaga',
        'nis', 'ipk', 'rapot', 'ujian', 'atasan', 'wali', 'wali kelas',
        'pra primer', 'pendidikan anak', 'tk', 'paud',
    ]
    task_domains = [k for k in domain_kw if k in task_lower]

    results = []
    for agent in agents:
        content = agent['content'].lower()
        score = 0
        matched = []
        # 1) Task-domain keyword (high weight)
        for k in task_domains:
            if k in content:
                score += 5
                matched.append('domain')
        # 2) Category keyword from task
        for cat, pattern in DEFAULT_CATEGORIES.items():
            if re.search(pattern, task_lower):
                score += 3
                matched.append(cat)
        # 3) Agent mentions the task's domain keywords
        for k in task_domains:
            if k in content and k not in matched:
                score += 2
                matched.append('agent-domain')
        # 4) Generic match (low weight)
        for cat, pattern in DEFAULT_CATEGORIES.items():
            if re.search(pattern, content):
                score += 1
        if score == 0:
            continue
        results.append((agent, score, matched))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


def print_result(results):
    if not results:
        print("Tidak ada agen yang cocok. Coba deskripsi yang lebih spesifik.")
        return
    print("=== KATEGORI KONTEKS ===")
    # Print categories that matched
    matched_cats = set()
    for _, _, cats in results:
        for c in cats:
            matched_cats.add(c)
    print("Categories matched:", ", ".join(sorted(matched_cats)) if matched_cats else "(none)")
    print("\n=== AGEN TERBAIK (top {}) ===".format(len(results)))
    for i, (agent, score, cats) in enumerate(results, 1):
        print(f"\n[{i}] {agent['name']} ({agent['file']})  score={score}")
        print(f"    Desc: {agent['description']}")
        print(f"    Kategori: {', '.join(cats)}")
        print(f"    Path: {agent['path']}")
        # Show first line of why it matches
        preview = agent['content'][:120].replace('\n', ' | ')
        print(f"    Preview: {preview}...")


def main():
    if len(sys.argv) < 2 or sys.argv[1] == '--list':
        print("=== DAFTAR AGEN (agents/) ===")
        agents = load_agents()
        for i, a in enumerate(agents, 1):
            print(f"  {i:>3}. {a['name']:<30} {a['description'][:60]}")
        if len(sys.argv) > 1 and sys.argv[1] == '--list':
            return
        print(f"\nTotal agen: {len(agents)}")
        print("\nContoh penggunaan:")
        print("  python3 context_router.py 'implement API nilai murid'")
        print("  python3 context_router.py 'review kode login'")
        print("  python3 context_router.py 'export laporan rapor PDF'")
        return

    task = sys.argv[1]
    agents = load_agents()
    if not agents:
        return
    results = match_agents(agents, task, top_n=6)
    print_result(results)


if __name__ == '__main__':
    main()
