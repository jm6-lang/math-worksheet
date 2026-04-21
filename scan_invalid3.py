import os, re

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs'
dirs = ['tools', 'self-media', 'book', 'movies', 'AIknowledge', 'curriculum', 'edu-knowlege', 'chinese-traditional']

# The "invalid" files are those where:
# 1. frontmatter has source: "" (empty) or no source field at all
# 2. AND body has no download links
# These are template/placeholder files with no real content

invalid_files = []
checked_files = []

for d in dirs:
    dpath = os.path.join(repo, d)
    if not os.path.exists(dpath):
        continue
    files = [f for f in os.listdir(dpath) if f.endswith('.md') and f != 'index.md']
    
    for f in files:
        fp = os.path.join(dpath, f)
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                raw = fh.read()
            
            content = raw.strip()
            # Split frontmatter
            if not content.startswith('---'):
                continue
            end = content.find('\n---\n', 4)
            if end == -1:
                end = content.find('\n---', 4)
            if end == -1:
                continue
            frontmatter = content[3:end].strip()
            body = content[end+4:].strip()
            
            # Get frontmatter fields
            source_m = re.search(r'^source:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
            source = source_m.group(1).strip().strip('"\'') if source_m else ''
            
            title_m = re.search(r'^title:\s*(.+?)\s*$', frontmatter, re.MULTILINE)
            title = title_m.group(1).strip().strip('"\'') if title_m else ''
            
            # Check body for links
            quark = re.findall(r'pan\.quark\.cn/s/\w+', body)
            xunlei = re.findall(r'xunlei\.com/s/\w+', body)
            
            # Determine if this file has valid content
            has_valid_link = (len(quark) > 0 or len(xunlei) > 0) and any(len(l) > 15 for l in quark + xunlei)
            
            info = {
                'rel': f'{d}/{f}',
                'source': source,
                'title': title,
                'quark': quark,
                'xunlei': xunlei,
                'has_valid_link': has_valid_link,
                'body_len': len(body),
            }
            
            if not has_valid_link and not source:
                invalid_files.append(info)
            
            checked_files.append(info)
        except Exception as e:
            pass

print(f'Total checked: {len(checked_files)}')
print(f'Files with no source AND no valid download links: {len(invalid_files)}')
print()
# Show invalid ones
for item in sorted(invalid_files, key=lambda x: x['rel']):
    print(f"  {item['rel']}: title='{item['title']}' body_len={item['body_len']}")

# Save
import json
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\invalid_files.json', 'w', encoding='utf-8') as f:
    json.dump({'invalid': invalid_files, 'checked': [{k:v for k,v in i.items() if k!="rel"} for i in checked_files]}, f, ensure_ascii=False, indent=2)
