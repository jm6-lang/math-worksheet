import re
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\skillxm_home2.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Find all link tags
links = re.findall(r'<link[^>]+>', html)
print('All link tags:')
for l in links:
    if 'stylesheet' in l or 'css' in l.lower():
        print(l)
