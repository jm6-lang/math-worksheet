import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script using picsum.photos
create_cmd = '''cat > /www/wwwroot/resource_site/img_fetch_v2.py << 'ENDSCRIPT'
#!/usr/bin/env python3
import requests, re, time, random

WP_URL = "https://skillxm.cn"
WP_TOKEN = "s6eW2kHy8yquXNuYJjoKHHOR"

def get_posts():
    headers = {"Authorization": "Basic " + WP_TOKEN}
    posts = []
    for page in range(1, 8):
        r = requests.get(WP_URL + "/wp-json/wp/v2/posts?per_page=100&page=" + str(page), headers=headers, timeout=30)
        if r.status_code == 200:
            for p in r.json():
                title = re.sub(r"<[^>]+>", "", p["title"]["rendered"])
                posts.append({"id": p["id"], "title": title})
    return posts

def get_random_img():
    # Use picsum.photos for random images
    img_id = random.randint(1, 1000)
    return "https://picsum.photos/seed/" + str(img_id) + "/800/600"

def dl_img(url):
    try:
        r = requests.get(url, timeout=20)
        return r.content if r.status_code == 200 else None
    except:
        return None

def upload_img(data):
    try:
        files = {"file": ("article_" + str(int(time.time())) + ".jpg", data, "image/jpeg")}
        r = requests.post(WP_URL + "/wp-json/wp/v2/media", 
                         headers={"Authorization": "Basic " + WP_TOKEN}, 
                         files=files, timeout=30)
        return r.json().get("id") if r.status_code in [200, 201] else None
    except Exception as e:
        print("    Upload error: " + str(e))
        return None

def set_thumb(post_id, img_id):
    try:
        r = requests.post(WP_URL + "/wp-json/wp/v2/posts/" + str(post_id), 
                         headers={"Authorization": "Basic " + WP_TOKEN, "Content-Type": "application/json"}, 
                         json={"featured_media": img_id}, timeout=30)
        return r.status_code in [200, 201]
    except Exception as e:
        print("    Set thumb error: " + str(e))
        return False

print("Getting posts...")
posts = get_posts()
print("Found: " + str(len(posts)) + " posts")

success = 0
fail = 0

for i, p in enumerate(posts[:50]):
    print("[" + str(i+1) + "/50] " + p["title"][:45])
    
    img_url = get_random_img()
    print("    URL: " + img_url[:60])
    
    data = dl_img(img_url)
    if data:
        print("    Downloaded: " + str(len(data)) + " bytes")
        img_id = upload_img(data)
        if img_id:
            if set_thumb(p["id"], img_id):
                print("    SUCCESS")
                success += 1
            else:
                print("    FAIL: set featured")
                fail += 1
        else:
            print("    FAIL: upload")
            fail += 1
    else:
        print("    FAIL: download")
        fail += 1
    
    time.sleep(1)

print("\n=== RESULTS ===")
print("Success: " + str(success))
print("Failed: " + str(fail))
print("Done")
ENDSCRIPT
'''

stdin, stdout, stderr = ssh.exec_command(create_cmd, timeout=15)
print("Script created")

# Run it
print("\nRunning Picsum image fetcher (50 posts)...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 img_fetch_v2.py 2>&1",
    timeout=300
)

output = stdout.read().decode('utf-8', errors='replace')
errors = stderr.read().decode('utf-8', errors='replace')

print(output)
if errors:
    print("Errors:", errors[:500])

ssh.close()