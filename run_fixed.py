import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create fixed script
script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为现有文章搜索并下载相关图片"""
import requests
import json
import re
import time
import random
import os
from urllib.parse import quote

WP_URL = "https://skillxm.cn"
WP_TOKEN = "s6eW 2kHy 8yqu XNuY JjoK HHOR"

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.4 Safari/605.1.15",
]

def get_posts():
    """获取所有文章"""
    headers = {
        "Authorization": "Basic " + WP_TOKEN.replace(" ", ""),
        "Content-Type": "application/json"
    }
    
    posts = []
    page = 1
    while True:
        try:
            r = requests.get(WP_URL + "/wp-json/wp/v2/posts?per_page=100&page=" + str(page), 
                           headers=headers, timeout=30)
            if r.status_code != 200:
                break
            data = r.json()
            if not data:
                break
            for p in data:
                title_clean = re.sub(r"<[^>]+>", "", p["title"]["rendered"])
                content_clean = re.sub(r"<[^>]+>", "", p["content"]["rendered"])[:200]
                posts.append({
                    "id": p["id"],
                    "title": title_clean,
                    "content": content_clean
                })
            page += 1
            if page > 10:
                break
        except Exception as e:
            print("Get posts error:", e)
            break
    return posts

def search_image(keyword):
    """使用Bing图片搜索"""
    try:
        kw = keyword[:25] if len(keyword) > 25 else keyword
        url = "https://www.bing.com/images/search?q=" + quote(kw) + "&form=HDRSC2&first=1"
        
        headers = {
            "User-Agent": random.choice(UAS),
            "Accept": "text/html",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        
        # Extract image URLs from Bing results
        matches = re.findall(r'murl":"(https?://[^"]+\.(?:jpg|jpeg|png|webp))', r.text, re.IGNORECASE)
        if matches:
            for img_url in matches[:5]:
                if img_url and len(img_url) > 10 and "bing" not in img_url.lower():
                    return img_url
        return None
    except Exception as e:
        print("Search error:", e)
        return None

def download_image(img_url):
    """下载图片"""
    try:
        headers = {"User-Agent": random.choice(UAS)}
        r = requests.get(img_url, headers=headers, timeout=15)
        if r.status_code == 200:
            content_type = r.headers.get("Content-Type", "")
            if "image" in content_type:
                return r.content, content_type
        return None, None
    except Exception as e:
        print("Download error:", e)
        return None, None

def upload_to_wp(image_data, content_type):
    """上传到WordPress"""
    headers = {
        "Authorization": "Basic " + WP_TOKEN.replace(" ", "")
    }
    
    try:
        ext = "jpg"
        if "png" in content_type:
            ext = "png"
        elif "webp" in content_type:
            ext = "webp"
        
        filename = "article_" + str(int(time.time())) + "." + ext
        files = {"file": (filename, image_data, content_type)}
        
        r = requests.post(WP_URL + "/wp-json/wp/v2/media", 
                         headers=headers, files=files, timeout=30)
        if r.status_code in [200, 201]:
            return r.json().get("id")
        return None
    except Exception as e:
        print("Upload error:", e)
        return None

def set_featured_image(post_id, image_id):
    """设置特色图片"""
    headers = {
        "Authorization": "Basic " + WP_TOKEN.replace(" ", ""),
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.post(WP_URL + "/wp-json/wp/v2/posts/" + str(post_id), 
                         headers=headers, 
                         json={"featured_media": image_id},
                         timeout=30)
        return r.status_code in [200, 201]
    except Exception as e:
        print("Set featured error:", e)
        return False

if __name__ == "__main__":
    print("Getting posts...")
    posts = get_posts()
    print("Found " + str(len(posts)) + " posts")
    
    # Process first 20 posts as test
    limit = min(20, len(posts))
    for i, post in enumerate(posts[:limit]):
        print("\n[" + str(i+1) + "/" + str(limit) + "] " + post["title"][:50])
        
        # Search image
        img_url = search_image(post["title"])
        
        if img_url:
            print("  Found: " + img_url[:60])
            
            # Download
            img_data, content_type = download_image(img_url)
            if img_data:
                # Upload
                img_id = upload_to_wp(img_data, content_type)
                
                if img_id:
                    # Set featured
                    if set_featured_image(post["id"], img_id):
                        print("  OK - Featured image set (ID: " + str(img_id) + ")")
                    else:
                        print("  FAIL - Could not set featured image")
                else:
                    print("  FAIL - Upload failed")
            else:
                print("  FAIL - Download failed")
        else:
            print("  FAIL - No image found")
        
        time.sleep(2)
    
    print("\nTest complete!")
'''

# Save script
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/fetch_images_fixed.py', 'w') as f:
    f.write(script)
sftp.close()

ssh.exec_command("chmod +x /www/wwwroot/resource_site/fetch_images_fixed.py")

# Run it
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 fetch_images_fixed.py 2>&1",
    timeout=180
)

print("Running... (this may take a few minutes)")
print("=" * 60)

# Read output
output = ""
while not stdout.channel.exit_status_ready():
    if stdout.channel.recv_ready():
        chunk = stdout.channel.recv(1024).decode('utf-8', errors='replace')
        output += chunk
        print(chunk, end='')

# Get any remaining
remaining = stdout.read().decode('utf-8', errors='replace')
if remaining:
    output += remaining
    print(remaining)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("Errors:", err)

print("=" * 60)
print("Done!")

ssh.close()