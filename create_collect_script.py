import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create a script to collect images for existing posts
collect_script = '''#!/usr/bin/env python3
"""为现有文章采集图片"""
import requests
import json
import re
import sys
import os

WP_URL = "https://skillxm.cn"
WP_TOKEN = "s6eW 2kHy 8yqu XNuY JjoK HHOR"

def get_posts_without_images():
    """获取没有特色图片的文章"""
    headers = {
        "Authorization": f"Basic {WP_TOKEN.replace(' ', '')}",
        "Content-Type": "application/json"
    }
    
    # Get posts
    posts = []
    page = 1
    while True:
        r = requests.get(f"{WP_URL}/wp-json/wp/v2/posts?per_page=100&page={page}&_embed", headers=headers, timeout=30)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        for p in data:
            # Check if has featured image
            if not p.get('featured_media'):
                posts.append({
                    'id': p['id'],
                    'title': p['title']['rendered'],
                    'content': p['content']['rendered'],
                    'categories': p.get('categories', [])
                })
        page += 1
        if page > 10:  # Limit
            break
    return posts

def search_image(keyword):
    """搜索相关图片 - 使用占位图服务"""
    # 根据关键词返回分类图片
    keyword_lower = keyword.lower()
    
    categories = {
        '小说': 'novel',
        '影视': 'movie',
        '电影': 'movie',
        '网赚': 'money',
        '赚钱': 'money',
        '教程': 'course',
        'AI': 'ai',
        'PPT': 'ppt',
    }
    
    for cn, en in categories.items():
        if cn in keyword:
            return f"{WP_URL}/wp-content/uploads/2026/04/category_{en}.png"
    
    return f"{WP_URL}/wp-content/uploads/2026/04/category_default.png"

def upload_image_to_wp(image_url):
    """上传图片到WordPress媒体库"""
    headers = {
        "Authorization": f"Basic {WP_TOKEN.replace(' ', '')}"
    }
    
    try:
        # Download image
        r = requests.get(image_url, timeout=15)
        if r.status_code != 200:
            return None
        
        # Upload to WP
        filename = os.path.basename(image_url)
        files = {'file': (filename, r.content, 'image/png')}
        
        upload_r = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            headers=headers,
            files=files,
            timeout=30
        )
        
        if upload_r.status_code in [200, 201]:
            return upload_r.json().get('id')
        return None
    except Exception as e:
        print(f"Upload error: {e}")
        return None

def set_featured_image(post_id, image_id):
    """设置文章特色图片"""
    headers = {
        "Authorization": f"Basic {WP_TOKEN.replace(' ', '')}",
        "Content-Type": "application/json"
    }
    
    r = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
        headers=headers,
        json={"featured_media": image_id},
        timeout=30
    )
    return r.status_code in [200, 201]

if __name__ == "__main__":
    print("获取没有特色图片的文章...")
    posts = get_posts_without_images()
    print(f"找到 {len(posts)} 篇文章没有特色图片")
    
    for post in posts[:50]:  # 处理前50篇
        print(f"处理: {post['title'][:40]}...")
        
        # 搜索相关图片
        img_url = search_image(post['title'])
        
        # 上传到媒体库
        img_id = upload_image_to_wp(img_url)
        if img_id:
            # 设置为特色图片
            if set_featured_image(post['id'], img_id):
                print(f"  ✓ 已设置特色图片")
            else:
                print(f"  ✗ 设置失败")
        else:
            print(f"  ✗ 上传失败")
        
        import time
        time.sleep(1)
    
    print("完成!")
'''

# Save script
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/collect_images.py', 'w') as f:
    f.write(collect_script)
sftp.close()

# Make executable
stdin, stdout, stderr = ssh.exec_command(
    "chmod +x /www/wwwroot/resource_site/collect_images.py",
    timeout=10
)

print("脚本已创建: /www/wwwroot/resource_site/collect_images.py")

# Run it
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 collect_images.py 2>&1",
    timeout=120
)
print("\n运行结果:")
print(stdout.read().decode('utf-8', errors='replace')[:2000])

ssh.close()