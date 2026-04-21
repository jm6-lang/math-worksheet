import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script content
script_content = '''#!/usr/bin/env python3
import requests, re, time, random

WP_URL = "https://skillxm.cn"
WP_TOKEN = "s6eW2kHy8yquXNuYJjoKHHOR"

def get_posts():
    headers = {"Authorization": "Basic " + WP_TOKEN}
    posts = []
    for page in range(1, 3):
        r = requests.get(WP_URL + "/wp-json/wp/v2/posts?per_page=100&page=" + str(page), headers=headers, timeout=30)
        if r.status_code == 200:
            for p in r.json():
                title = re.sub(r"<[^>]+>", "", p["title"]["rendered"])
                posts.append({"id": p["id"], "title": title})
    return posts

def get_img_url():
    try:
        r = requests.get("https://source.unsplash.com/800x600/?technology,business", timeout=20, allow_redirects=True)
        return r.url if r.status_code == 200 else None
    except:
        return None

def dl_img(url):
    try:
        return requests.get(url, timeout=20).content
    except:
        return None

def upload_img(data):
    try:
        files = {"file": ("img.jpg", data, "image/jpeg")}
        r = requests.post(WP_URL + "/wp-json/wp/v2/media", headers={"Authorization": "Basic " + WP_TOKEN}, files=files, timeout=30)
        return r.json().get("id") if r.status_code in [200, 201] else None
    except:
        return None

def set_thumb(post_id, img_id):
    try:
        r = requests.post(WP_URL + "/wp-json/wp/v2/posts/" + str(post_id), headers={"Authorization": "Basic " + WP_TOKEN, "Content-Type": "application/json"}, json={"featured_media": img_id}, timeout=30)
        return r.status_code in [200, 201]
    except:
        return False

print("Getting posts...")
posts = get_posts()
print("Found: " + str(len(posts)))

for i, p in enumerate(posts[:20]):
    print("[" + str(i+1) + "] " + p["title"][:40])
    img_url = get_img_url()
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
        print("  FAIL: get URL")
    time.sleep(2)

print("Done")
'''

# Write script using SFTP
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/img_fetch.py', 'w') as f:
    f.write(script_content)
sftp.close()

print("Script created via SFTP")

# Run it
print("\nRunning image fetcher...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 img_fetch.py 2>&1",
    timeout=300
)

output = stdout.read().decode('utf-8', errors='replace')
errors = stderr.read().decode('utf-8', errors='replace')

print(output)
if errors:
    print("Errors:", errors[:500])

ssh.close()