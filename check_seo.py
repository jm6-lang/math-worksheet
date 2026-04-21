import urllib.request
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Get homepage
r = urllib.request.urlopen('https://www.skillxm.cn/')
content = r.read().decode('utf-8')

# Extract title
title = re.search(r'<title>(.*?)</title>', content)
print('=== Title ===')
print(title.group(1) if title else 'Not found')

# Check meta description
desc = re.search(r'<meta name="description" content="([^"]*)"', content)
print('\n=== Meta Description ===')
print(desc.group(1)[:100] if desc else 'Not found')

# Check h1
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', content)
print('\n=== H1 ===')
print(h1.group(1) if h1 else 'Not found')

# Check site name
site_name = re.search(r'<meta property="og:site_name" content="([^"]*)"', content)
print('\n=== Site Name ===')
print(site_name.group(1) if site_name else 'Not found')

# Check schema
schema = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
print('\n=== Schema ===')
if schema:
    import json
    try:
        data = json.loads(schema.group(1))
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
    except:
        print(schema.group(1)[:300])