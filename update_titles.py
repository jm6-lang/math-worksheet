import os, re, json

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'

updates = [
    ('movies/post_127.md', '饭店常点的35个菜详细视频教学', 'movies'),
    ('movies/post_128.md', '招牌菜36道现学视频教程', 'movies'),
    ('curriculum/post_034.md', '厨师长教你做菜系列视频教程', 'curriculum'),
    ('curriculum/post_035.md', '精品凉拌菜系统卤味系统课程', 'curriculum'),
]

for fn, new_title, d in updates:
    fp = os.path.join(repo, d, fn.split('/')[-1]) if '/' in fn else os.path.join(repo, d, fn)
    if not os.path.exists(fp):
        print(f'NOT FOUND: {fp}')
        continue
    
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check if already has proper Chinese title (not garbled)
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', new_title))
    
    # Update frontmatter title
    content_new = re.sub(
        r'^title:\s*["\']?.+?["\']?\s*$',
        f'title: "{new_title}"',
        content,
        count=1,
        flags=re.MULTILINE
    )
    
    # Update first h1 heading
    content_new = re.sub(
        r'^#\s+.+$',
        f'# {new_title}',
        content_new,
        count=1,
        flags=re.MULTILINE
    )
    
    # Also update Badge tip text in body
    content_new = re.sub(
        r'(<Badge[^>]*text=)"[^"]*"',
        rf'\1"{new_title}"',
        content_new,
        count=1
    )
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print(f'Updated: {fp} -> {new_title}')

print('\nDone.')
