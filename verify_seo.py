import urllib.request
import re

# Verify homepage meta
r = urllib.request.urlopen('https://www.skillxm.cn/')
content = r.read().decode('utf-8')

print('=== 检查SEO输出 ===')

# Look for schema
if 'schema.org' in content:
    print('Schema.org: OK')

# Look for meta description
desc = re.search(r'<meta name="description" content="([^"]*)"', content)
if desc:
    print(f'Meta Description: {desc.group(1)[:80]}')
else:
    print('Meta Description: MISSING')

# Look for canonical
canonical = re.search(r'<link rel="canonical" href="([^"]*)"', content)
if canonical:
    print(f'Canonical: {canonical.group(1)}')
else:
    print('Canonical: MISSING')

# Check sitemap
r2 = urllib.request.urlopen('https://www.skillxm.cn/robots.txt')
robots = r2.read().decode('utf-8')
if 'Sitemap:' in robots:
    for line in robots.split('\n'):
        if 'Sitemap:' in line:
            print(f'robots.txt: {line}')

# Check sitemap index
r3 = urllib.request.urlopen('https://www.skillxm.cn/sitemap_index.xml')
sm = r3.read().decode('utf-8')
sitemap_count = sm.count('<sitemap>')
print(f'Sitemap files: {sitemap_count}')

print('\n=== SEO基础检查完成 ===')