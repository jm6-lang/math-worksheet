import requests
import re

r = requests.get('https://www.skycaiji.com/', timeout=15)
content = r.text

# Find download links
links = re.findall(r'href=["\']([^"\']+)["\']', content)
for link in links:
    if any(kw in link.lower() for kw in ['download', 'zip', 'tar', 'github', 'skycaiji', 'down', 'install']):
        print(link)

# Also check for version info
version = re.findall(r'version[=:"\' ]+([0-9.]+)', content, re.I)
if version:
    print("\n版本:", version[:3])

# Check page title
title = re.search(r'<title>([^<]+)</title>', content)
if title:
    print("\n标题:", title.group(1))
