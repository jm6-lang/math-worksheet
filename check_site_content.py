import urllib.request

req = urllib.request.Request('https://skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
r = urllib.request.urlopen(req, timeout=15)
html = r.read().decode('utf-8', errors='ignore')

print('Page length:', len(html))
print('Has posts:', 'post-item' in html)
print('Post count:', html.count('post-item'))

# Check for navigation menu
nav_start = html.find('<nav')
if nav_start > 0:
    nav_end = html.find('</nav>', nav_start)
    print('\nNavigation area:')
    print(html[nav_start:nav_end][:1000])

# Check for category links
print('\nCategory links found:')
for cat in ['fuye', 'chuangye', 'wangzhuan', 'zimeiti']:
    if f'/category/{cat}' in html:
        print(f'  - {cat}: Found')
    else:
        print(f'  - {cat}: Not found')