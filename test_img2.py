import requests, re, time

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
API_TOKEN = "s6eW 2kHy 8yqu XNuY JjoK HHOR"

# Test: Get a Wikimedia image directly
test_file = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/800px-Camponotus_flavomarginatus_ant.jpg"
r = requests.head(test_file, timeout=10, headers={'User-Agent': USER_AGENT})
print(f"Direct Wikimedia: {r.status_code} | {r.headers.get('Content-Type','')} | Size: {r.headers.get('Content-Length','?')}")

# Test WordPress media upload
print("\nTest WordPress media upload:")
SITE = "https://skillxm.cn"
test_img = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Camponotus_flavomarginatus_ant.jpg/400px-Camponotus_flavomarginatus_ant.jpg"
img_data = requests.get(test_img, timeout=15, headers={'User-Agent': USER_AGENT})
print(f"Image download: {img_data.status_code} | size={len(img_data.content)}")

if img_data.status_code == 200:
    import base64
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'admin:{API_TOKEN}'.encode()).decode()}",
        "Content-Disposition": "attachment; filename=test_img.jpg",
        "Content-Type": "image/jpeg",
    }
    r3 = requests.post(
        f"{SITE}/wp-json/wp/v2/media",
        headers=headers,
        data=img_data.content,
        timeout=20,
    )
    print(f"WP upload: {r3.status_code} | {r3.text[:300]}")

# Test Bing image search
print("\nBing image search:")
url = "https://www.bing.com/images/search?q=online+course+learning+free&first=0&count=5"
r4 = requests.get(url, timeout=10, headers={
    'User-Agent': USER_AGENT,
})
matches = re.findall(r'"murl":"([^"]+)"', r4.text)
print(f"Found {len(matches)} image URLs")
for m in matches[:3]:
    print(f"  {m[:100]}")
