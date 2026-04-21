import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create script to search and download relevant images for existing posts
script = '''#!/usr/bin/env python3
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
        "Authorization": f"Basic {WP_TOKEN.replace(' ', '')}",
        "Content-Type": "application/json"
    }
    
    posts = []
    page = 1
    while True:
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts?per_page=100&page={page}", headers=headers, timeout=30)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        for p in data:
            posts.append({
                'id': p['id'],
                'title': re.sub(r'<[^>]+>', '', p['title']['rendered']),
                'content': re.sub(r'<[^>]+>', '', p['content']['rendered'])[:200]
            })
        page += 1
        if page > 10:
            break
    return posts

def search_image_bing(keyword):
    """使用Bing图片搜索"""
    try:
        # 简化关键词
        kw = keyword[:20] if len(keyword) > 20 else keyword
        url = f"https://www.bing.com/images/search?q={quote(kw)}&form=HDRSC2&first=1"
        
        headers = {
            "User-Agent": random.choice(UAS),
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        
        # 提取图片URL
        # Bing图片搜索结果中的murl参数
        matches = re.findall(r'murl":"(https?://[^"]+\.(?:jpg|jpeg|png|webp))', r.text, re.IGNORECASE)
        if matches:
            # 返回第一个非空结果
            for img_url in matches[:5]:
                if img_url and len(img_url) > 10:
                    return img_url
        return None
    except Exception as e:
        print(f"  Search error: {e}")
        return None

def search_image_duckduckgo(keyword):
    """使用DuckDuckGo图片搜索作为备选"""
    try:
        kw = quote(keyword[:30])
        url = f"https://duckduckgo.com/?q={kw}&iax=images&ia=images"
        
        headers = {
            "User-Agent": random.choice(UAS),
            "Accept": "text/html"
        }
        
        r = requests.get(url, headers=headers, timeout=15)
        # 提取图片URL
        matches = re.findall(r'https?://[^\s"<>]+\.(?:jpg|jpeg|png)', r.text, re.IGNORECASE)
        return matches[0] if matches else None
    except:
        return None

def download_image(img_url):
    """下载图片"""
    try:
        headers = {"User-Agent": random.choice(UAS)}
        r = requests.get(img_url, headers=headers, timeout=15, stream=True)
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            if 'image' in content_type:
                return r.content
        return None
    except Exception as e:
        print(f"  Download error: {e}")
        return None

def upload_to_wp(image_data, filename):
    """上传到WordPress"""
    headers = {
        "Authorization": f"Basic {WP_TOKEN.replace(' ', '')}"
    }
    
    try:
        files = {'file': (filename, image_data, 'image/jpeg')}
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=headers, files=files, timeout=30)
        if r.status_code in [200, 201]:
            return r.json().get('id')
        return None
    except Exception as e:
        print(f"  Upload error: {e}")
        return None

def set_featured_image(post_id, image_id):
    """设置特色图片"""
    headers = {
        "Authorization": f"Basic {WP_TOKEN.replace(' ', '')}",
        "Content-Type": "application/json"
    }
    
    try:
        r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts/{post_id}", 
                         headers=headers, 
                         json={"featured_media": image_id},
                         timeout=30)
        return r.status_code in [200, 201]
    except:
        return False

if __name__ == "__main__":
    print("获取文章列表...")
    posts = get_posts()
    print(f"找到 {len(posts)} 篇文章")
    
    # 处理前20篇作为测试
    for i, post in enumerate(posts[:20]):
        print(f"\n[{i+1}/{min(20,len(posts))}] {post['title'][:50]}...")
        
        # 搜索图片
        img_url = search_image_bing(post['title'])
        if not img_url:
            img_url = search_image_duckduckgo(post['title'])
        
        if img_url:
            print(f"  找到图片: {img_url[:60]}...")
            
            # 下载
            img_data = download_image(img_url)
            if img_data:
                # 上传
                ext = img_url.split('.')[-1].split('?')[0][:4] or 'jpg'
                filename = f"post_{post['id']}_{int(time.time())}.{ext}"
                img_id = upload_to_wp(img_data, filename)
                
                if img_id:
                    # 设置特色图片
                    if set_featured_image(post['id'], img_id):
                        print(f"  ✓ 成功设置特色图片 (ID: {img_id})")
                    else:
                        print(f"  ✗ 设置失败")
                else:
                    print(f"  ✗ 上传失败")
            else:
                print(f"  ✗ 下载失败")
        else:
            print(f"  ✗ 未找到图片")
        
        time.sleep(2)  # 避免请求过快
    
    print("\n测试完成!")
'''

# Save script
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/fetch_post_images.py', 'w') as f:
    f.write(script)
sftp.close()

# Make executable
ssh.exec_command("chmod +x /www/wwwroot/resource_site/fetch_post_images.py")

print("脚本已创建: /www/wwwroot/resource_site/fetch_post_images.py")
print("\n这个脚本会:")
print("1. 获取所有文章")
print("2. 根据文章标题搜索相关图片 (Bing/DuckDuckGo)")
print("3. 下载图片并上传到WordPress")
print("4. 设置为文章特色图片")
print("\n是否运行测试 (处理前20篇文章)?")

ssh.close()