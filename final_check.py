import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# Confirm the 36 invalid files + verify movies/post_106 is actually valid
check_files = [
    'AIknowledge/post_024.md',
    'AIknowledge/post_026.md',
    'AIknowledge/post_027.md',
    'AIknowledge/post_028.md',
    'AIknowledge/post_033.md',
    'AIknowledge/post_034.md',
    'AIknowledge/post_035.md',
    'AIknowledge/post_037.md',
    'AIknowledge/post_039.md',
    'AIknowledge/post_047.md',
    'AIknowledge/post_048.md',
    'AIknowledge/post_052.md',
    'AIknowledge/post_055.md',
    'AIknowledge/post_056.md',
    'book/post_015.md',
    'book/post_018.md',
    'book/post_025.md',
    'curriculum/post_009.md',
    'curriculum/post_010.md',
    'curriculum/post_011.md',
    'curriculum/post_012.md',
    'curriculum/post_013.md',
    'curriculum/post_017.md',
    'curriculum/post_023.md',
    'curriculum/post_027.md',
    'curriculum/post_068.md',
    'curriculum/post_073.md',
    'curriculum/post_077.md',
    'curriculum/post_079.md',
    'curriculum/post_082.md',
    'curriculum/post_083.md',
    'curriculum/post_085.md',
    'curriculum/post_095.md',
    'curriculum/post_103.md',
    'edu-knowlege/post_013.md',
    'movies/post_010.md',
    'movies/post_098.md',
    'movies/post_099.md',
    'movies/post_106.md',  # verify
    'movies/post_107.md',
    'movies/post_110.md',
    'movies/post_111.md',
    'movies/post_112.md',
    'movies/post_124.md',
    'self-media/post_003.md',
    'self-media/post_006.md',
    'tools/post_002.md',
    'tools/post_008.md',
    'tools/post_026.md',
    'tools/post_047.md',
    'tools/post_063.md',
    'tools/post_075.md',
    'tools/post_087.md',
    'tools/post_124.md',
]

to_delete = []
for rel in check_files:
    fp = os.path.join(repo, rel)
    if not os.path.exists(fp):
        print(f'{rel}: NOT FOUND (already deleted)')
        continue
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
    
    # Broad link detection
    links = re.findall(r'pan\.(?:quark\.cn|baidu\.com)|xunlei\.com|alipan\.com', body, re.I)
    
    if links:
        print(f'VALID: {rel} -> links: {set(links)}')
    else:
        print(f'INVALID: {rel}')
        to_delete.append(rel)

print(f'\nWill delete {len(to_delete)} files')
for f in to_delete:
    print(f'  {f}')
