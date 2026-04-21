import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script using Unsplash API (no key needed for demo)
create_cmd = '''cat > /www/wwwroot/resource_site/img_fetcher2.py << 'EOF'
#!/usr/bin/env python3
import requests, re, time, random
from urllib.parse import quote

WP_URL = "https://skillxm.cn"
WP_TOKEN = "s6eW2kHy8yquXNuYJjoKHHOR"

# Unsplash API - free, no key required for demo
UNSPLASH_API = "https://api.unsplash.com/search/photos"

UAS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]

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
            title = re.sub(r"<[^>]+>", "", p["title"]["rendered"])
            # Get category info
            cats = p.get("categories", [])
            posts.append({"id": p["id"], "title": title, "cats": cats})
    return posts

def get_cat_name(cat_id):
    try:
        headers = {"Authorization": "Basic " + WP_TOKEN}
        r = requests.get(WP_URL + "/wp-json/wp/v2/categories/" + str(cat_id), headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json().get("name", "")
    except:
        pass
    return ""

def search_unsplash(keyword):
    """Search Unsplash for images"""
    try:
        # Use source.unsplash.com for random images by keyword
        # Format: https://source.unsplash.com/800x600/?keyword
        search_terms = {
            "小说": "book,novel",
            "影视": "movie,film,cinema",
            "电影": "movie,cinema",
            "网赚": "money,business",
            "赚钱": "money,finance",
            "教程": "education,learning",
            "AI": "artificial,intelligence,technology",
            "PPT": "presentation,business",
            "资源": "download,files",
            "项目": "project,work"
        }
        
        # Find matching search term
        term = "technology"  # default
        for k, v in search_terms.items():
            if k in keyword:
                term = v
                break
        
        # Get random image from Unsplash Source
        url = "https://source.unsplash.com/800x600/?" + quote(term)
        r = requests.get(url, headers={"User-Agent": random.choice(UAS)}, timeout=20, allow_redirects=True)
        if r.status_code == 200:
            return r.url  # Return final URL after redirect
        return None
    except Exception as e:
        print("  Unsplash error: " + str(e))
        return None

def dl_img(url):
    try:
        r = requests.get(url, headers={"User-Agent": random.choice(UAS)}, timeout=20)
        return r.content if r.status_code == 200 else None
    except:
        return None

def upload_img(data):
    try:
        files = {"file": ("article.jpg", data, "image/jpeg")}
        r = requests.post(WP_URL + "/wp-json/wp/v2/media", 
                         headers={"Authorization": "Basic " + WP_TOKEN},
                         files=files, timeout=30)
        return r.json().get("id") if r.status_code in [200, 201] else None
    except Exception as e:
        print("  Upload error: " + str(e))
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
print("Found: " + str(len(posts)) + " posts")

success = 0
failed = 0

for i, p in enumerate(posts[:30]):  # Test with 30 posts
    print("[" + str(i+1) + "] " + p["title"][:40])
    
    # Try to get category-based image
    img_url = search_unsplash(p["title"])
    
    if img_url:
        print("  Found: " + img_url[:50])
        data = dl_img(img_url)
        if data:
            print("  Downloaded: " + str(len(data)) + " bytes")
            img_id = upload_img(data)
            if img_id:
                if set_thumb(p["id"], img_id):
                    print("  OK - Set featured image")
                    success += 1
                else:
                    print("  FAIL - Could not set featured")
                    failed += 1
            else:
                print("  FAIL - Upload failed")
                failed += 1
        else:
            print("  FAIL - Download failed")
            failed += 1
    else:
        print("  FAIL - No image found")
        failed += 1
    
    time.sleep(1.5)

print("\n=== Results ===")
print("Success: " + str(success))
print("Failed: " + str(failed))
print("Done")
EOF
'''

stdin, stdout, stderr = ssh.exec_command(create_cmd, timeout=15)
print("Script created")

# Run it
print("\nRunning Unsplash image fetcher (30 posts test)...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 img_fetcher2.py 2>&1",
    timeout=300
)

output = stdout.read().decode('utf-8', errors='replace')
errors = stderr.read().decode('utf-8', errors='replace')

print(output)
if errors:
    print("Errors:", errors[:500])

ssh.close()