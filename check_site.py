import urllib.request

r = urllib.request.urlopen('https://skillxm.cn/', timeout=15)
html = r.read().decode('utf-8', errors='ignore')

print('Length:', len(html))
print('Has puock:', 'puock' in html.lower())
print('Has article/post:', 'article' in html.lower() or 'post-' in html.lower())

# Find main content area
content_start = html.find('id="content"')
if content_start > 0:
    print('\nContent area found at position:', content_start)
    print(html[content_start:content_start+2000])
else:
    print('\nNo content area found')
    # Look for other main areas
    for marker in ['class="container', 'id="main', 'class="main']:
        pos = html.find(marker)
        if pos > 0:
            print(f'\nFound {marker} at position:', pos)
            print(html[pos:pos+1000])
            break