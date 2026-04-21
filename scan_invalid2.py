import os, re, json

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

# Find files where the body has no valid download links (no pan.quark.cn or similar)
invalid_files = []

for d in dirs:
    dpath = os.path.join(repo, d)
    if not os.path.exists(dpath):
        continue
    files = [f for f in os.listdir(dpath) if f.endswith('.md') and f != 'index.md']
    
    for f in files:
        fp = os.path.join(dpath, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            
            body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
            
            # Look for download links in body
            quark_links = re.findall(r'pan\.quark\.cn/[^\s<>"\']+', body)
            xunlei_links = re.findall(r'xunlei\.com[^\s<>"\']+', body)
            
            # A file is "invalid" if it has no real download links in body
            has_valid_link = len(quark_links) > 0 or len(xunlei_links) > 0
            
            title_m = re.search(r'^---\s*\ntitle:\s*["\']?(.+?)["\']?\s*\n', content, re.MULTILINE)
            title = title_m.group(1).strip() if title_m else ''
            has_chinese = bool(re.search(r'[\u4e00-\u9fff]', title))
            
            if not has_valid_link:
                invalid_files.append({
                    'rel': f'{d}/{f}',
                    'title': title,
                    'has_chinese': has_chinese,
                    'body_len': len(body),
                })
        except Exception as e:
            pass

print(f'Files with NO valid download links: {len(invalid_files)}')
print()
for item in sorted(invalid_files, key=lambda x: x['rel']):
    print(f"  {item['rel']}: title='{item['title']}' chinese={item['has_chinese']} body={item['body_len']}")

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\invalid_files.json', 'w', encoding='utf-8') as f:
    json.dump(invalid_files, f, ensure_ascii=False, indent=2)
