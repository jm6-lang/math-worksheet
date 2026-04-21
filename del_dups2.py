import os, subprocess
from collections import defaultdict
import re

base = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal'

primary_prefixes = ['tcm/', 'curriculum/', 'AIknowledge/', 'self-media/', 'movies/']
title_map = defaultdict(list)

for root, dirs, files in os.walk(base):
    for fname in files:
        if not fname.endswith('.md') or fname in ['_index.md', 'index.md', '目录.md']:
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, base).replace('\\', '/')
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            for line in content.split('\n')[:10]:
                ls = line.strip()
                if ls.startswith('title:'):
                    t = ls.split('title:', 1)[1].strip().strip('"').strip("'")
                    title_map[t].append(rel)
                    break
        except Exception as e:
            pass

def get_num(path):
    m = re.search(r'_(\d+)\.md$|post_(\d+)\.md$', path)
    return int(m.group(1) or m.group(2)) if m else 99999

to_delete = []

for title, files in title_map.items():
    if len(files) <= 1:
        continue
    primary_files = [f for f in files if any(f.startswith(p) for p in primary_prefixes)]
    if primary_files:
        for f in files:
            if f not in primary_files:
                to_delete.append(f)
    else:
        files_sorted = sorted(files, key=lambda f: get_num(f))
        for f in files_sorted[1:]:
            to_delete.append(f)

# Internal dups
to_delete.extend(['book/post_027.md', 'curriculum/post_108.md'])

to_delete = sorted(set(to_delete))
print('Files to delete:', len(to_delete))

ok_count = 0
fail_count = 0
for f in to_delete:
    full = 'docs/' + f
    r = subprocess.run(['git', 'rm', '--', full], cwd=repo, capture_output=True, text=True)
    if r.returncode == 0:
        ok_count += 1
    else:
        fail_count += 1
        print('FAIL:', full, r.stderr[:80])

print('OK:', ok_count, 'FAIL:', fail_count)
