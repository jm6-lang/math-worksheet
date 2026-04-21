import requests, re

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'

tests = []

# Test 1: DuckDuckGo image search API
try:
    url = f"https://duckduckgo.com/?q=free+stock+image&ia=web"
    r = requests.get(url, timeout=10, headers={'User-Agent': USER_AGENT})
    matches = re.findall(r'"image":"(https?://[^"]+\.(?:jpg|jpeg|png))"', r.text)
    if not matches:
        matches = re.findall(r'imgurl=(https?://[^&"\'\s]+\.(?:jpg|jpeg|png))', r.text)
    tests.append(f"DuckDuckGo images: {len(matches)} found")
    for m in matches[:2]:
        tests.append(f"  {m[:100]}")
except Exception as e:
    tests.append(f"DuckDuckGo: {e}")

# Test 2: Google image search (no key)
try:
    url = "https://www.google.com/search?tbm=isch&q=free+stock+photo&btnG=Search+Images"
    r = requests.get(url, timeout=10, headers={'User-Agent': USER_AGENT})
    matches = re.findall(r'"ou":"(https?://[^"]+\.(?:jpg|jpeg|png))"', r.text)
    if not matches:
        matches = re.findall(r'src="(https?://[^"]+\.(?:jpg|jpeg|png))"', r.text[:50000])
    tests.append(f"Google images: {len(matches)} found")
    for m in matches[:2]:
        tests.append(f"  {m[:100]}")
except Exception as e:
    tests.append(f"Google images: {e}")

# Test 3: LoremFlickr
try:
    url = "https://loremflickr.com/800/600/business,online?lock=1"
    r = requests.head(url, timeout=10, allow_redirects=True)
    loc = r.headers.get('Location', '')
    tests.append(f"LoremFlickr: {r.status_code} | {loc[:100]}")
except Exception as e:
    tests.append(f"LoremFlickr: {e}")

# Test 4: Plati.ru free images
try:
    # Try a free CDN image
    url = "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800"
    r = requests.head(url, timeout=10, allow_redirects=True)
    tests.append(f"Unsplash direct: {r.status_code} | {r.headers.get('Content-Type','')}")
except Exception as e:
    tests.append(f"Unsplash direct: {e}")

# Test 5: Placeholder with gradient (no external)
try:
    url = "https://httpbin.org/image/jpeg"
    r = requests.get(url, timeout=10)
    tests.append(f"HTTPBin image: {r.status_code} | size={len(r.content)}")
except Exception as e:
    tests.append(f"HTTPBin image: {e}")

# Test 6: WordPress native placeholder
try:
    url = "https://skillxm.cn/wp-admin/images/wordpress-logo.svg"
    r = requests.head(url, timeout=8)
    tests.append(f"WP placeholder: {r.status_code} | {r.headers.get('Content-Type','')}")
except Exception as e:
    tests.append(f"WP placeholder: {e}")

for t in tests:
    print(t)
