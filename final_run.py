import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script using cat heredoc
create_cmd = '''cat > /www/wwwroot/resource_site/img_fetcher.py << 'EOF'
#!/usr/bin/env python3
import requests, re, time, random
from urllib.parse import quote

WP_URL = "https://skillxm.cn"
WP_TOKEN = "s6eW2kHy8yquXNuYJjoKHHOR"
UAS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36"]

def get_posts():
    headers = {"Authorization": "Basic " + WP_TOKEN, "Content-Type": "application/json"}
    posts = []
    for page in range(1, 11):
        r = requests.get(WP_URL + "/wp-json/wp/v2/posts?per_page=100&page=" + str(page), headers=headers, timeout=30)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        for p in data:
            posts.append({"id": p["id"], "title": re.sub(r"<[^>]+>", "", p["title"]["rendered"])})
    return posts

def search_img(kw):
    try:
        url = "https://www.bing.com/images/search?q=" + quote(kw[:25]) + "&form=HDRSC2"
        r = requests.get(url, headers={"User-Agent": random.choice(UAS)}, timeout=15)
        m = re.findall(r'murl":"(https?://[^"]+\\.(?:jpg|jpeg|png))', r.text, re.I)
        return m[0] if m else None
    except:
        return None

def dl_img(url):
    try:
        r = requests.get(url, headers={"User-Agent": random.choice(UAS)}, timeout=15)
        return r.content if r.status_code == 200 else None
    except:
        return None

def upload_img(data):
    try:
        files = {"file": ("img.jpg", data, "image/jpeg")}
        r = requests.post(WP_URL + "/wp-json/wp/v2/media", 
                         headers={"Authorization": "Basic " + WP_TOKEN},
                         files=files, timeout=30)
        return r.json().get("id") if r.status_code in [200, 201] else None
    except:
        return None

def set_thumb(post_id, img_id):
    try:
        r = requests.post(WP_URL + "/wp-json/wp/v2/posts/" + str(post_id),
                         headers={"Authorization": "Basic " + WP_TOKEN, "Content-Type": "application/json"},
                         json={"featured_media": img_id}, timeout=30)
        return r.status_code in [200, 201]
    except:
        return False

print("Getting posts...")
posts = get_posts()
print("Found: " + str(len(posts)))

for i, p in enumerate(posts[:20]):
    print("[" + str(i+1) + "] " + p["title"][:40])
    img_url = search_img(p["title"])
    if img_url:
        data = dl_img(img_url)
        if data:
            img_id = upload_img(data)
            if img_id and set_thumb(p["id"], img_id):
                print("  OK")
            else:
                print("  FAIL: upload/set")
        else:
            print("  FAIL: download")
    else:
        print("  FAIL: search")
    time.sleep(2)

print("Done")
EOF
'''

stdin, stdout, stderr = ssh.exec_command(create_cmd, timeout=15)
print("Script created")

# Run it
print("\nRunning...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 img_fetcher.py 2>&1",
    timeout=180
)

output = stdout.read().decode('utf-8', errors='replace')
errors = stderr.read().decode('utf-8', errors='replace')

print(output)
if errors:
    print("Errors:", errors)

ssh.close()