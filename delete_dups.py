import os, subprocess, time
from collections import defaultdict

base = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# Primary directories (authoritative sources to KEEP)
primary_prefixes = [
    'tcm/',
    'curriculum/',
    'AIknowledge/',
    'self-media/',
    'movies/',
]

# Internal dups to fix: (keep, delete)
internal_dups = {
    'book/post_027.md': 'book/post_026.md',   # keep 026, del 027
    'curriculum/post_108.md': 'curriculum/post_107.md',  # keep 107, del 108
}

title_map = defaultdict(list)

for root, dirs, files in os.walk(base):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        if fname in ['_index.md', 'index.md', '目录.md']:
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, base).replace('\\', '/')
        
        try:
            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            title = None
            for line in content.split('\n')[:10]:
                ls = line.strip()
                if ls.startswith('title:'):
                    t = ls.split('title:', 1)[1].strip().strip('"').strip("'")
                    title = t
                    break
            if title:
                title_map[title].append(rel)
        except Exception as e:
            pass

# Determine files to delete
to_delete = []

for title, files in title_map.items():
    if len(files) <= 1:
        continue
    
    # Check if there are primary-dir files among the dups
    primary_files = [f for f in files if any(f.startswith('docs/' + p) for p in primary_prefixes)]
    
    if primary_files:
        # Has primary source: delete everything else (non-primary dups)
        for f in files:
            if f not in primary_files:
                # Check it's not in internal_dups keeper
                is_keeper = any(f == keeper for keeper in internal_dups.values())
                if not is_keeper:
                    to_delete.append(f)
    else:
        # No primary source: keep the one with lowest number
        import re
        def get_num(path):
            m = re.search(r'_(\d+)\.md$|post_(\d+)\.md$', path)
            return int(m.group(1) or m.group(2)) if m else 99999
        
        files_sorted = sorted(files, key=lambda f: get_num(f))
        keep = files_sorted[0]
        for f in files_sorted[1:]:
            is_keeper = any(f == keeper for keeper in internal_dups.values())
            if not is_keeper:
                to_delete.append(f)

# Add internal dups that should be deleted
for del_file, keep_file in internal_dups.items():
    full_del = 'docs/' + del_file
    if full_del not in to_delete:
        to_delete.append(full_del)

to_delete = sorted(to_delete)
print(f'Total files to delete: {len(to_delete)}')
for f in to_delete:
    print(f'  DEL {f}')

# Now do the git rm
repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal'
for f in to_delete:
    full_path = os.path.join(repo, f)
    if os.path.exists(full_path):
        r = subprocess.run(['git', 'rm', '--', f], cwd=repo, capture_output=True, text=True)
        if r.returncode == 0:
            print(f'  rm OK: {f}')
        else:
            print(f'  rm FAIL: {f} - {r.stderr[:80]}')
    else:
        print(f'  NOT FOUND (already removed?): {f}')

print('\nDone. Run git status and git commit to complete.')
