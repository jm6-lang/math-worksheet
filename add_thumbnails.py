import paramiko
import sys
import json
import time
import random
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 先看看数据库里有多少图片，以及文章总数
print("=== 数据库状态 ===\n")
check_cmds = [
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT COUNT(*) as total_posts FROM wp_posts WHERE post_type='post' AND post_status='publish';\" 2>/dev/null",
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT COUNT(*) as with_thumb FROM wp_postmeta WHERE meta_key='_thumbnail_id' AND meta_value > 0;\" 2>/dev/null",
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT COUNT(*) as total_media FROM wp_posts WHERE post_type='attachment';\" 2>/dev/null",
    "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID DESC LIMIT 10;\" 2>/dev/null",
]
for cmd in check_cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    print(stdout.read().decode('utf-8', errors='ignore').strip())

# 用关键词生成不同的占位图颜色/样式
# 根据文章标题hash选择不同的图片样式
def get_image_urls(count):
    """为多篇文章生成不同的占位图URL"""
    base_urls = [
        "https://placehold.co/800x500/2563eb/ffffff?text={}",
        "https://placehold.co/800x500/059669/ffffff?text={}",
        "https://placehold.co/800x500/d97706/ffffff?text={}",
        "https://placehold.co/800x500/dc2626/ffffff?text={}",
        "https://placehold.co/800x500/7c3aed/ffffff?text={}",
        "https://placehold.co/800x500/0891b2/ffffff?text={}",
        "https://placehold.co/800x500/be185d/ffffff?text={}",
        "https://placehold.co/800x500/4338ca/ffffff?text={}",
    ]
    # 使用unsplash的固定图片，更美观
    unsplash_ids = [
        "photo-1460925895917-afdab827c52f",  # workspace
        "photo-1504384308090-c894fdcc538d",  # tech
        "photo-1551288049-bebda4e38f71",  # data
        "photo-1517694712202-14dd9538aa97",  # laptop
        "photo-1461749280684-dccba630e2f6",  # code
        "photo-1559136555-9303baea8ebd",  # colorful
        "photo-1498050108023-c5249f4df085",  # screen
        "photo-1516321318423-f06f85e504b3",  # abstract
        "photo-1526374965328-7f61d4dc18c5",  # matrix
        "photo-1537432376149-e8937dfb6564",  # modern
        "photo-1504639725590-34d0984388bd",  # design
        "photo-1522202176988-66273c2fd55f",  # team
        "photo-1432888498266-38ffec3eaf0a",  # neon
        "photo-1550751827-4bd374c3f58b",  # cyber
        "photo-1535223289827-42f1e9919769",  # social
        "photo-1553877522-43269d4ea984",  # money
    ]
    
    urls = []
    for i in range(count):
        idx = i % len(unsplash_ids)
        urls.append("https://images.unsplash.com/%s?w=800&h=500&fit=crop&auto=format" % unsplash_ids[idx])
    return urls

# 查找没有缩略图的文章
find_cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT p.ID FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id AND pm.meta_key = '_thumbnail_id' WHERE p.post_type='post' AND p.post_status='publish' AND pm.meta_value IS NULL ORDER BY p.ID DESC LIMIT 20;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(find_cmd, timeout=15)
no_thumb = stdout.read().decode('utf-8', errors='ignore').strip().split('\n')
no_thumb = [x.strip() for x in no_thumb if x.strip()]
print("\n=== 需要配图的文章: %d篇 ===" % len(no_thumb))

if not no_thumb:
    print("所有文章都有缩略图！")
    ssh.close()
    sys.exit(0)

# 生成配图并写入数据库
# 先看现有图片ID范围
cmd = "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT MIN(ID), MAX(ID), COUNT(*) FROM wp_posts WHERE post_type='attachment';\" 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
range_info = stdout.read().decode('utf-8', errors='ignore').strip()
print("媒体库ID范围: %s" % range_info)

# 用Python生成缩略图 - 下载unsplash图片然后通过WP上传
script = r'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import urllib.request
import os
import sys

WP_PATH = "/www/wwwroot/resource_site"
POST_IDS = %s

def download_image(url, filepath):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(filepath, "wb") as f:
                f.write(data)
            return True
    except Exception as e:
        # fallback to placehold.co
        try:
            fallback = "https://placehold.co/800x500/2563eb/ffffff?text=Article"
            req = urllib.request.Request(fallback, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(filepath, "wb") as f:
                    f.write(data)
                return True
        except:
            return False

def set_thumbnail(post_id, media_id):
    cmd = "cd %s && wp post meta update %d _thumbnail_id %d --allow-root 2>/dev/null" % (WP_PATH, post_id, media_id)
    subprocess.run(cmd, shell=True, capture_output=True, timeout=10)

def upload_media(filepath):
    cmd = "cd %s && wp media import %s --porcelain --allow-root 2>/dev/null" % (WP_PATH, filepath)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    if result.stdout.strip().isdigit():
        return int(result.stdout.strip())
    return 0

# Unsplash 固定图片列表
IMAGES = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1537432376149-e8937dfb6564?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1535223289827-42f1e9919769?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?w=800&h=500&fit=crop&auto=format",
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=500&fit=crop&auto=format",
]

success = 0
fail = 0
for i, post_id in enumerate(POST_IDS):
    idx = int(post_id) %% len(IMAGES)
    img_url = IMAGES[idx]
    tmp_path = "/tmp/thumb_%%d.jpg" %% int(post_id)
    
    sys.stdout.write("  Post %%s: " %% post_id)
    sys.stdout.flush()
    
    if download_image(img_url, tmp_path):
        media_id = upload_media(tmp_path)
        if media_id > 0:
            set_thumbnail(int(post_id), media_id)
            print("+ media_id=%d" %% media_id)
            success += 1
        else:
            print("- upload failed")
            fail += 1
        # cleanup
        try:
            os.remove(tmp_path)
        except:
            pass
    else:
        print("- download failed")
        fail += 1
    
    import time
    time.sleep(1)

print("\nDone: %d success, %d fail" %% (success, fail))
''' % no_thumb[:20]

# 上传脚本到服务器
sftp = ssh.open_sftp()
with sftp.open('/tmp/add_thumbnails.py', 'w') as f:
    f.write(script)
sftp.close()

print("\n=== 开始为文章添加缩略图 ===\n")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/add_thumbnails.py 2>&1', timeout=600)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
