import paramiko
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 直接写脚本到服务器
script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import urllib.request
import os
import time

WP_PATH = "/www/wwwroot/resource_site"

IMAGES = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1537432376149-e8937dfb6564?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=500&fit=crop",
]

def download_image(url, filepath):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) < 5000:
                raise Exception("Too small")
            with open(filepath, "wb") as f:
                f.write(data)
            return True
    except Exception as e:
        fb = "https://placehold.co/800x500/2563eb/ffffff?text=Resource"
        try:
            req = urllib.request.Request(fb, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                with open(filepath, "wb") as f:
                    f.write(data)
                return True
        except:
            return False

# Get posts without thumbnails
cmd = (
    'mysql -u wp_user -p"gMshA29CshK5" wp_skillxm -N -e '
    '"SELECT p.ID FROM wp_posts p '
    'LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id AND pm.meta_key = \'_thumbnail_id\' '
    'WHERE p.post_type=\'post\' AND p.post_status=\'publish\' AND pm.meta_value IS NULL '
    'ORDER BY p.ID DESC LIMIT 20;" 2>/dev/null'
)
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
post_ids = [x.strip() for x in result.stdout.strip().split('\\n') if x.strip()]
print("Need thumbnails: %d posts" % len(post_ids))

success = 0
for i, pid in enumerate(post_ids):
    idx = int(pid) % len(IMAGES)
    img_url = IMAGES[idx]
    tmp = "/tmp/thumb_%s.jpg" % pid
    
    print("Post %s: " % pid, end="")
    
    if download_image(img_url, tmp):
        # Upload via WP-CLI
        cmd = 'cd %s && wp media import "%s" --porcelain --allow-root 2>/dev/null' % (WP_PATH, tmp)
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        mid = r.stdout.strip()
        if mid.isdigit():
            # Set thumbnail
            cmd2 = 'cd %s && wp post meta update %s _thumbnail_id %s --allow-root 2>/dev/null' % (WP_PATH, pid, mid)
            subprocess.run(cmd2, shell=True, capture_output=True, timeout=10)
            print("OK (media=%s)" % mid)
            success += 1
        else:
            print("FAIL upload: %s" % r.stdout[:50])
    else:
        print("FAIL download")
    
    try:
        os.remove(tmp)
    except:
        pass
    time.sleep(1)

print("\\nResult: %d/%d success" % (success, len(post_ids)))
'''

sftp = ssh.open_sftp()
with sftp.open('/tmp/add_thumbs.py', 'w') as f:
    f.write(script_content)
sftp.close()
print("脚本已上传")

print("\n=== 开始添加缩略图 ===")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/add_thumbs.py 2>&1', timeout=600)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
