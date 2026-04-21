import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 使用服务器端Python采集 ===\n")

# 创建完整脚本
script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import feedparser
import subprocess
import time
import re

RSS = [
    "https://www.36kr.com/feed",
    "https://sspai.com/feed", 
    "https://www.ithome.com/rss/IT",
]

def clean(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.DOTALL)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.DOTALL)
    t = re.sub(r'<[^>]+>', '', t)
    return t.strip()

def post(title, content, cat):
    with open('/tmp/pc.txt', 'w') as f:
        f.write(content)
    t = title.replace('"', '\\\\"')
    cmd = f'cd /www/wwwroot/resource_site && wp post create --post_type=post --post_title="{t}" --post_content="$(cat /tmp/pc.txt)" --post_category={cat} --post_status=publish --allow-root 2>&1'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if 'Success' in r.stdout or 'created' in r.stdout.lower():
        print(f"OK: {title[:30]}...")
        return True
    print(f"FAIL: {r.stdout[:80]}")
    return False

print("=== Collecting ===")
c = 0
for url in RSS:
    print(f"RSS: {url.split('/')[2]}")
    try:
        f = feedparser.parse(url)
        for e in f.entries[:2]:
            t = e.title if hasattr(e, 'title') else "No Title"
            c2 = e.summary if hasattr(e, 'summary') else t
            c2 = clean(c2)
            if len(c2) < 50:
                c2 = c2 + "\\n\\n" + (e.link if hasattr(e, 'link') else "")
            c2 = f"<p>整理自网络</p><div>{c2}</div><p>来源: {e.link if hasattr(e, 'link') else ''}</p>"
            if post(t, c2, 7):
                c += 1
                time.sleep(2)
            if c >= 6: break
        if c >= 6: break
    except Exception as ex:
        print(f"Error: {str(ex)}")
    time.sleep(2)
print(f"Done! Total: {c}")
'''

# 上传脚本
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/wpcrawl.py', 'w') as f:
    f.write(script)
sftp.close()

print("1. Script uploaded")

# 设置权限
ssh.exec_command("chmod +x /www/wwwroot/resource_site/auto_collect/wpcrawl.py", timeout=10)
print("2. Permissions set")

# 运行
print("\n3. Running...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 wpcrawl.py 2>&1", timeout=180)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
