import urllib.request, re, sys, json

url = "https://docs.skillxm.cn/nav.html"
try:
    with urllib.request.urlopen(url, timeout=10) as r:
        data = r.read().decode("utf-8", errors="replace")
except Exception as e:
    print(f"Failed to fetch: {e}")
    sys.exit(1)

# Extract VP_HASH_MAP
m = re.search(r'window\.__VP_HASH_MAP__=JSON\.parse\("(.+?)"\)', data)
if not m:
    print("No hash map found")
    sys.exit(0)

raw = m.group(1).replace('\\"', '"')
try:
    hm = json.loads(raw)
except Exception as e:
    print(f"JSON parse error: {e}")
    sys.exit(0)

# Check nav and healthy
nav_keys = [k for k in hm if "nav" in k.lower()]
healthy_keys = [k for k in hm if "healthy" in k.lower()]
print(f"Total keys: {len(hm)}")
print(f"nav keys: {nav_keys}")
print(f"healthy keys: {healthy_keys}")
# Also check all index keys
idx_keys = [k for k in hm if "_index" in k]
print(f"index keys: {idx_keys}")
