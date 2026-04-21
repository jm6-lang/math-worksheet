import os

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

# All confirmed blank template files (500-600 bytes, no real content)
to_delete = [
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
    'chinese-traditional/ziwei.md',
    'curriculum/post_009.md',
    'curriculum/post_010.md',
    'curriculum/post_011.md',
    'curriculum/post_012.md',
    'curriculum/post_013.md',
    'curriculum/post_017.md',
    'curriculum/post_023.md',
    'curriculum/post_027.md',
    'curriculum/post_062.md',
    'curriculum/post_065.md',
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
    'movies/post_098.md',
    'movies/post_099.md',
    'movies/post_106.md',
    'movies/post_107.md',
    'movies/post_110.md',
    'movies/post_111.md',
    'movies/post_112.md',
    'movies/post_124.md',
    'self-media/post_003.md',
    'self-media/post_006.md',
    'self-media/post_011.md',
    'tools/post_002.md',
    'tools/post_006.md',
    'tools/post_007.md',
    'tools/post_008.md',
    'tools/post_012.md',
    'tools/post_013.md',
    'tools/post_014.md',
    'tools/post_017.md',
    'tools/post_018.md',
    'tools/post_019.md',
    'tools/post_020.md',
    'tools/post_021.md',
    'tools/post_022.md',
    'tools/post_023.md',
    'tools/post_026.md',
    'tools/post_039.md',
    'tools/post_047.md',
    'tools/post_060.md',
    'tools/post_063.md',
    'tools/post_067.md',
    'tools/post_071.md',
    'tools/post_075.md',
    'tools/post_082.md',
    'tools/post_084.md',
    'tools/post_087.md',
    'tools/post_099.md',
    'tools/post_101.md',
    'tools/post_124.md',
]

# Also ziwei.md special - it's the ziwei divination page, check if it has real content
ziwei_fp = os.path.join(repo, 'chinese-traditional', 'ziwei.md')
if os.path.exists(ziwei_fp):
    with open(ziwei_fp, encoding='utf-8', errors='ignore') as f:
        z = f.read()
    body = z.replace(z[:z.find('\n---', 4)+5 if '---' in z[:10] else len(z)], '').strip()
    if 'iztro' in body or 'ZiWeiCalculator' in body or len(body) > 1000:
        print('chinese-traditional/ziwei.md has real content - SKIPPING')
        to_delete.remove('chinese-traditional/ziwei.md')

count = 0
for rel in to_delete:
    fp = os.path.join(repo, rel)
    if os.path.exists(fp):
        os.remove(fp)
        print(f'Deleted: {rel}')
        count += 1
    else:
        print(f'Not found: {rel}')

print(f'\nTotal deleted: {count}')

# Build git remove commands
print('\nGit commands to stage:')
for rel in to_delete:
    fp = os.path.join(repo, rel)
    if os.path.exists(fp):
        print(f'already deleted above')
    else:
        print(f'docs/{rel}')
