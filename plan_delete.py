import subprocess, base64, json

# Files to delete: (path, sha)
# Build this by scanning all files and grouping by title

def get_all_files():
    """Get all files from repo tree"""
    r = subprocess.run(
        ['gh', 'api', 'repos/jm6-lang/resource-portal/git/trees/main?recursive=1',
         '--jq', '.tree[].path'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    paths = r.stdout.strip().split('\n')
    return [p for p in paths if p.startswith('docs/') and p.endswith('.md')]

def get_title_content(path):
    r = subprocess.run(
        ['gh', 'api', 'repos/jm6-lang/resource-portal/contents/' + path,
         '--jq', '{content: .content, sha: .sha}'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    try:
        data = json.loads(r.stdout)
        raw = data['content'].strip()
        content = base64.b64decode(raw).decode('utf-8', errors='replace')
        sha = data['sha']
        for line in content.split('\n')[:8]:
            ls = line.strip()
            if ls.startswith('title:'):
                t = ls.split('title:', 1)[1].strip().strip('"').strip("'")
                return t, sha
        return None, sha
    except:
        return None, None

print('Getting all files...')
all_files = get_all_files()
print('Total files:', len(all_files))

# Collect titles
from collections import defaultdict
title_map = defaultdict(list)  # title -> [(path, sha)]

for i, path in enumerate(all_files):
    if i % 20 == 0:
        print(f'  {i}/{len(all_files)}...')
    
    title, sha = get_title_content(path)
    if title and sha:
        title_map[title].append((path, sha))

# Find dups and decide what to delete
# Primary sources (keep): tcm/, curriculum/, AIknowledge/, self-media/
# Also keep one from curriculum internal dups
primary_dirs = {'docs/tcm/', 'docs/curriculum/', 'docs/AIknowledge/', 'docs/self-media/', 'docs/movies/'}

# For book/ internal dups: keep lower number
# For curriculum/ internal dups: keep lower number

to_delete = []  # [(path, sha, reason)]

for title, files in title_map.items():
    if len(files) <= 1:
        continue
    
    # Sort: prefer primary dirs, then by path number
    def sort_key(item):
        path = item[0]
        # Prefer primary directories
        is_primary = any(path.startswith(d) for d in primary_dirs)
        # Extract number for sorting
        import re
        nums = re.findall(r'_(\d+)\.md$|post_(\d+)\.md$|tcm_(\d+)\.md$', path)
        num = 99999
        for m in nums:
            for g in m:
                if g:
                    num = int(g)
                    break
            if num < 99999:
                break
        return (0 if is_primary else 1, num, path)
    
    files_sorted = sorted(files, key=sort_key)
    keep = files_sorted[0]
    for path, sha in files_sorted[1:]:
        to_delete.append((path, sha, title))

print(f'\nFiles to delete: {len(to_delete)}')
for path, sha, title in to_delete[:20]:
    print(f'  DEL {path}  ({title[:30]})')
if len(to_delete) > 20:
    print(f'  ... and {len(to_delete)-20} more')

# Save to file for confirmation
with open('to_delete.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total files to delete: {len(to_delete)}\n\n')
    for path, sha, title in to_delete:
        f.write(f'{path}\t{sha}\t{title}\n')

print('\nSaved to to_delete.txt')
