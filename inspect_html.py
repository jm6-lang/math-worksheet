import re
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\skillxm_home2.html', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print('HTML size:', len(html))
print('First 500 chars:')
print(html[:500])
print('\n...')
print('Last 500 chars:')
print(html[-500:])
