import sys
import urllib.request
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')

# Extract ALL ld+json schemas
schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
print("Total JSON-LD: %d" % len(schemas))

for i, s in enumerate(schemas):
    try:
        data = json.loads(s)
        if '@graph' in data:
            print("\n#%d: @graph with %d items" % (i+1, len(data['@graph'])))
            for item in data['@graph']:
                print("  - %s: %s" % (item.get('@type','?'), item.get('name','')[:40]))
        else:
            print("\n#%d: %s" % (i+1, data.get('@type','?')))
            print("  name: %s" % data.get('name','')[:60])
            if 'mainEntity' in data:
                for e in data['mainEntity']:
                    print("  Q: %s" % e.get('name','')[:60])
    except Exception as e:
        print("\n#%d: ERROR - %s" % (i+1, str(e)[:60]))
        print("  Raw: %s" % s[:100])

# Check for geo meta
meta_author = re.findall(r'<meta[^>]*name="author"[^>]*>', body)
print("\nMeta author tags: %d" % len(meta_author))
robots_meta = re.findall(r'<meta[^>]*name="robots"[^>]*content="([^"]*)"', body)
print("Meta robots: %s" % robots_meta[:3])
