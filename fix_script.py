import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== Fix and Run Collector ===\n")

script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import feedparser
import requests
import time
import re

WP_URL = "https://skillxm.cn/wp-json/wp/v2"
API_TOKEN = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
CATEGORY_ID = 7

RSS_FEEDS = [
    {"name": "36kr", "url": "https://www.36kr.com/feed"},
    {"name": "sspai", "url": "https://sspai.com/feed"},
    {"name": "ithome", "url": "https://www.ithome.com/rss/IT"},
]

def post_wp(title, content, cat):
    h = {"Authorization": "Bearer " + API_TOKEN, "Content-Type": "application/json"}
    d = {"title": title, "content": content, "status": "publish", "categories": [cat]}
    r = requests.post(WP_URL + "/posts", headers=h, json=d, timeout=30)
    if r.status_code in [200, 201]:
        print("OK:", title[:30])
        return True
    print("FAIL:", r.status_code, r.text[:100])
    return False

def clean(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.DOTALL)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.DOTALL)
    t = re.sub(r'<[^>]+>', '', t)
    return t.strip()

def main():
    print("=== Collect Start ===")
    count = 0
    for f in RSS_FEEDS:
        try:
            print("Feed:", f["name"])
            feed = feedparser.parse(f["url"])
            for e in feed.entries[:2]:
                if not hasattr(e, 'link'): continue
                c = e.summary if hasattr(e, 'summary') else e.title
                c = clean(c)
                if len(c) < 50: c = c + " - " + e.link
                c = "<p>内容整理自网络</p><div>" + c + "</div><p>来源: " + e.link + "</p>"
                title = e.title if hasattr(e, 'title') else "No Title"
                if post_wp(title, c, CATEGORY_ID):
                    count += 1
                    time.sleep(2)
                if count >= 6: break
            if count >= 6: break
        except Exception as ex:
            print("Error:", str(ex))
    print("Total:", count)

if __name__ == "__main__": main()
"""

# Write file
sftp = ssh.open_sftp()
f = sftp.open('/www/wwwroot/resource_site/auto_collect/collector_v3.py', 'w')
f.write(script)
f.close()
print("1. Script updated")

# Run
print("\n2. Running...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector_v3.py 2>&1", timeout=180)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
