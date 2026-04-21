import os, re, json

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

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
            
            # Check source link
            source_m = re.search(r'source:\s*["\']?([^"\'\n]+)["\']?', content)
            source = source_m.group(1).strip() if source_m else ''
            
            # Check if source is empty or broken
            is_invalid = False
            if not source or source.strip() == '':
                is_invalid = True
            elif 'pan.quark.cn' in source and ('#' in source or '无' in source or source.count('/') < 3):
                is_invalid = True
            
            # Check if file has ANY body content (not just frontmatter)
            body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL | re.MULTILINE).strip()
            has_real_content = len(body) > 10 and not all(c in ' \n\t#<>:|-\u3000' for c in body)
            
            # Check title is garbled (only Chinese-adjacent bytes, no real chars)
            title_m = re.search(r'^---\s*\ntitle:\s*["\']?(.+?)["\']?\s*\n', content, re.MULTILINE)
            title = title_m.group(1).strip() if title_m else ''
            is_garbled = title and not re.search(r'[\u4e00-\u9fff]', title)
            
            if is_invalid:
                invalid_files.append({
                    'path': fp,
                    'relative': f'{d}/{f}',
                    'source': source,
                    'has_body': has_real_content,
                    'is_garbled': is_garbled,
                    'title': title
                })
        except Exception as e:
            pass

print(f'Found {len(invalid_files)} invalid files:')
for item in invalid_files:
    print(f"  {item['relative']}: source='{item['source']}' garbled={item['is_garbled']} body={item['has_body']}")

# Save for script
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\invalid_files.json', 'w', encoding='utf-8') as f:
    json.dump(invalid_files, f, ensure_ascii=False, indent=2)
print('\nSaved to invalid_files.json')
