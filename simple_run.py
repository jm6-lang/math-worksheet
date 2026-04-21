import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script with proper escaping
commands = [
    "cd /www/wwwroot/resource_site",
    "rm -f img_fetcher3.py",
    "echo '#!/usr/bin/env python3' > img_fetcher3.py",
    "echo 'import requests, re, time, random' >> img_fetcher3.py",
    "echo 'from urllib.parse import quote' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'WP_URL = \"https://skillxm.cn\"' >> img_fetcher3.py",
    "echo 'WP_TOKEN = \"s6eW2kHy8yquXNuYJjoKHHOR\"' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'def get_posts():' >> img_fetcher3.py",
    "echo '    headers = {\"Authorization\": \"Basic \" + WP_TOKEN}' >> img_fetcher3.py",
    "echo '    posts = []' >> img_fetcher3.py",
    "echo '    for page in range(1, 3):' >> img_fetcher3.py",
    "echo '        r = requests.get(WP_URL + \"/wp-json/wp/v2/posts?per_page=100&page=\" + str(page), headers=headers, timeout=30)' >> img_fetcher3.py",
    "echo '        if r.status_code == 200:' >> img_fetcher3.py",
    "echo '            for p in r.json():' >> img_fetcher3.py",
    "echo '                posts.append({\"id\": p[\"id\"], \"title\": re.sub(r\"<[^>]+>\", \"\", p[\"title\"][\"rendered\"])})' >> img_fetcher3.py",
    "echo '    return posts' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'def get_img_url():' >> img_fetcher3.py",
    "echo '    try:' >> img_fetcher3.py",
    "echo '        r = requests.get(\"https://source.unsplash.com/800x600/?technology\", timeout=20, allow_redirects=True)' >> img_fetcher3.py",
    "echo '        return r.url if r.status_code == 200 else None' >> img_fetcher3.py",
    "echo '    except: return None' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'def dl_img(url):' >> img_fetcher3.py",
    "echo '    try: return requests.get(url, timeout=20).content' >> img_fetcher3.py",
    "echo '    except: return None' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'def upload_img(data):' >> img_fetcher3.py",
    "echo '    try:' >> img_fetcher3.py",
    "echo '        files = {\"file\": (\"img.jpg\", data, \"image/jpeg\")}' >> img_fetcher3.py",
    "echo '        r = requests.post(WP_URL + \"/wp-json/wp/v2/media\", headers={\"Authorization\": \"Basic \" + WP_TOKEN}, files=files, timeout=30)' >> img_fetcher3.py",
    "echo '        return r.json().get(\"id\") if r.status_code in [200, 201] else None' >> img_fetcher3.py",
    "echo '    except: return None' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'def set_thumb(post_id, img_id):' >> img_fetcher3.py",
    "echo '    try:' >> img_fetcher3.py",
    "echo '        r = requests.post(WP_URL + \"/wp-json/wp/v2/posts/\" + str(post_id), headers={\"Authorization\": \"Basic \" + WP_TOKEN, \"Content-Type\": \"application/json\"}, json={\"featured_media\": img_id}, timeout=30)' >> img_fetcher3.py",
    "echo '        return r.status_code in [200, 201]' >> img_fetcher3.py",
    "echo '    except: return False' >> img_fetcher3.py",
    "echo '' >> img_fetcher3.py",
    "echo 'print(\"Getting posts...\")' >> img_fetcher3.py",
    "echo 'posts = get_posts()' >> img_fetcher3.py",
    "echo 'print(\"Found: \" + str(len(posts)))' >> img_fetcher3.py",
    "echo 'for i, p in enumerate(posts[:20]):' >> img_fetcher3.py",
    "echo '    print(\"[\" + str(i+1) + \"] \" + p[\"title\"][:40])' >> img_fetcher3.py",
    "echo '    img_url = get_img_url()' >> img_fetcher3.py",
    "echo '    if img_url:' >> img_fetcher3.py",
    "echo '        data = dl_img(img_url)' >> img_fetcher3.py",
    "echo '        if data:' >> img_fetcher3.py",
    "echo '            img_id = upload_img(data)' >> img_fetcher3.py",
    "echo '            if img_id and set_thumb(p[\"id\"], img_id):' >> img_fetcher3.py",
    "echo '                print(\"  OK\")' >> img_fetcher3.py",
    "echo '            else: print(\"  FAIL: upload/set\")' >> img_fetcher3.py",
    "echo '        else: print(\"  FAIL: download\")' >> img_fetcher3.py",
    "echo '    else: print(\"  FAIL: get URL\")' >> img_fetcher3.py",
    "echo '    time.sleep(2)' >> img_fetcher3.py",
    "echo 'print(\"Done\")' >> img_fetcher3.py",
]

for cmd in commands:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
    stdout.channel.recv_exit_status()

print("Script created")

# Run it
print("\nRunning...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 img_fetcher3.py 2>&1",
    timeout=300
)

output = stdout.read().decode('utf-8', errors='replace')
errors = stderr.read().decode('utf-8', errors='replace')

print(output)
if errors:
    print("Errors:", errors[:500])

ssh.close()