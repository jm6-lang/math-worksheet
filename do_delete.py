import os

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

to_delete = [
    'AIknowledge/post_024.md',
    'book/post_015.md',
    'book/post_025.md',
    'curriculum/post_009.md',
    'curriculum/post_010.md',
    'curriculum/post_011.md',
    'curriculum/post_012.md',
    'curriculum/post_013.md',
    'curriculum/post_023.md',
    'curriculum/post_027.md',
    'curriculum/post_068.md',
    'curriculum/post_073.md',
    'curriculum/post_077.md',
    'curriculum/post_079.md',
    'curriculum/post_082.md',
    'curriculum/post_085.md',
    'curriculum/post_095.md',
    'curriculum/post_103.md',
    'edu-knowlege/post_013.md',
    'movies/post_010.md',
    'movies/post_098.md',
    'movies/post_099.md',
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

git_cmds = []
for rel in to_delete:
    fp = os.path.join(repo, rel)
    if os.path.exists(fp):
        os.remove(fp)
        git_cmds.append(f'docs/{rel}')
        print(f'Deleted: {rel}')
    else:
        print(f'Not found: {rel}')

print(f'\nDeleted {len(git_cmds)} files')

# Write git commands to file for reference
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\git_del_cmds.txt', 'w') as f:
    for cmd in git_cmds:
        f.write(f'git rm {cmd}\n')
print('Git commands written to git_del_cmds.txt')
