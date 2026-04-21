import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 完整的采集脚本 - 带自动配图
collector = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auto collector with auto thumbnail - 副业赚钱教程"""
import feedparser
import subprocess
import time
import re
import os
import json
import urllib.request
from datetime import datetime

WP_PATH = "/www/wwwroot/resource_site"
CATEGORY_ID = 53  # 网赚项目
MAX_POSTS = 6
PUBLISHED_FILE = os.path.join(os.path.dirname(__file__), "published.json")
BAIDU_TOKEN = "zJsDaj5ibt8ZlVgz"
BAIDU_PUSH_URL = "http://data.zz.baidu.com/urls?site=https://www.skillxm.cn&token=" + BAIDU_TOKEN

RSS_FEEDS = [
    "https://www.aiyingli.com/feed",
    "https://www.woshipm.com/feed",
    "https://www.cyzone.cn/rss/",
    "https://sspai.com/feed",
    "https://www.v2ex.com/index.xml",
]

POSITIVE_KW = [
    "副业","赚钱","网赚","兼职","创业","项目","教程","变现","收入",
    "引流","私域","自媒体","短视频","直播","电商","拼多多","抖音",
    "闲鱼","小红书","公众号","流量","运营","SEO","带货","知识付费",
    "AI赚钱","AI变现","GPT","ChatGPT","AIGC","被动收入","理财",
    "投资","基金","接单","自由职业","远程办公","获客","转化","成交",
    "裂变","社群","模板","素材","工具","资源",
]

NEGATIVE_KW = [
    "融资","上市","IPO","财报","裁员","年报","股价","市值",
    "涨停","跌停","股市","机器人","芯片","半导体","新能源车",
]

# Unsplash图片用于自动配图
THUMB_IMAGES = [
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

def load_published():
    try:
        with open(PUBLISHED_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_published(urls):
    with open(PUBLISHED_FILE, "w") as f:
        json.dump(list(urls), f)

def clean_html(html):
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\\s+", " ", text)
    return text.strip()

def is_relevant(title, content=""):
    text = (title + " " + content).lower()
    for kw in NEGATIVE_KW:
        if kw in title:
            return False
    for kw in POSITIVE_KW:
        if kw in title or kw.lower() in text:
            return True
    return False

def download_image(url, filepath):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = r.read()
            if len(d) < 5000:
                raise Exception("too small")
            with open(filepath, "wb") as f:
                f.write(d)
            return True
    except:
        try:
            fb = "https://placehold.co/800x500/2563eb/ffffff?text=Resource"
            req = urllib.request.Request(fb, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                with open(filepath, "wb") as f:
                    f.write(r.read())
                return True
        except:
            return False

def set_thumbnail(post_id):
    """Download image and set as thumbnail"""
    idx = int(post_id) % len(THUMB_IMAGES)
    url = THUMB_IMAGES[idx]
    tmp = "/tmp/th_%s.jpg" % post_id
    if not download_image(url, tmp):
        return
    try:
        ci = "cd %s && wp media import \\"%s\\" --porcelain --allow-root 2>/dev/null" % (WP_PATH, tmp)
        ri = subprocess.run(ci, shell=True, capture_output=True, text=True, timeout=30)
        mid = ri.stdout.strip()
        if mid.isdigit():
            ct = "cd %s && wp post meta update %s _thumbnail_id %s --allow-root 2>/dev/null" % (WP_PATH, post_id, mid)
            subprocess.run(ct, shell=True, capture_output=True, timeout=10)
    except:
        pass
    try:
        os.remove(tmp)
    except:
        pass

def wp_post(title, content, cat_id):
    content_file = "/tmp/wp_post_content.txt"
    with open(content_file, "w", encoding="utf-8") as f:
        f.write(content)

    safe_title = title.replace("\\\\", "\\\\\\\\").replace('"', '\\\\"')
    cmd = (
        "cd %s && "
        'wp post create '
        '--post_type=post '
        '--post_title="%s" '
        '--post_content="$(cat %s)" '
        "--post_category=%d "
        "--post_status=publish "
        "--allow-root 2>&1"
    ) % (WP_PATH, safe_title, content_file, cat_id)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if "Success" in result.stdout:
            m = re.search(r"Created post (\\d+)", result.stdout)
            post_id = m.group(1) if m else "?"
            return True, post_id
        else:
            print("  WP Error: %s" % result.stdout[:80])
            return False, ""
    except Exception as e:
        print("  Exception: %s" % str(e))
        return False, ""

def push_baidu(urls):
    if not urls:
        return
    try:
        with open("/tmp/baidu_push.txt", "w") as f:
            f.write("\\n".join(urls))
        cmd = "curl -s --data-binary @/tmp/baidu_push.txt \\"%s\\" -H \\"Content-Type:text/plain\\" 2>/dev/null" % BAIDU_PUSH_URL
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout.strip():
            print("  Baidu: %s" % result.stdout.strip()[:100])
    except:
        pass

def main():
    print("[%s] Starting (副业赚钱 + auto thumbnail)..." % datetime.now().strftime("%Y-%m-%d %H:%M"))
    published = load_published()
    print("  Cache: %d" % len(published))

    new_urls = []
    total = 0
    skipped = 0

    for rss_url in RSS_FEEDS:
        print("\\n  RSS: %s" % rss_url.split("/")[2])
        try:
            feed = feedparser.parse(rss_url, request_headers={"User-Agent": "Mozilla/5.0"})
            if not feed.entries:
                print("    No entries")
                continue

            for entry in feed.entries[:5]:
                link = getattr(entry, "link", "")
                if not link or link in published:
                    continue

                title = getattr(entry, "title", "Untitled")
                summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or title

                if not is_relevant(title, summary):
                    skipped += 1
                    continue

                text = clean_html(summary)
                if len(text) < 80:
                    text = text + "\\n\\n" + link

                content = (
                    "<p>%s</p>"
                    '<p>来源: <a href="%s" target="_blank" rel="nofollow">查看原文</a></p>'
                ) % (text, link)

                ok, post_id = wp_post(title, content, CATEGORY_ID)
                if ok:
                    published.add(link)
                    # Auto set thumbnail
                    print("  + [%s] %s" % (post_id, title[:30]), end="", flush=True)
                    set_thumbnail(post_id)
                    print(" [thumb]")
                    new_urls.append("https://www.skillxm.cn/?p=%s" % post_id)
                    total += 1
                    time.sleep(2)

                if total >= MAX_POSTS:
                    break
        except Exception as e:
            print("    Error: %s" % str(e)[:50])

        if total >= MAX_POSTS:
            break

    save_published(published)

    if new_urls:
        print("\\n  Baidu push %d URLs..." % len(new_urls))
        push_baidu(new_urls)

    print("\\n  Result: %d published, %d skipped" % (total, skipped))
    return total

if __name__ == "__main__":
    main()
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(collector)
sftp.close()
print("1. 采集脚本已更新（带自动配图）")

# 清空缓存重新测试
ssh.exec_command("echo '[]' > /www/wwwroot/resource_site/auto_collect/published.json", timeout=5)
print("2. 缓存已清空")

# 测试
print("\n3. 测试运行（带自动配图）...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector.py 2>&1",
    timeout=300
)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
