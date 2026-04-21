import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 更新采集脚本（副业赚钱教程）===\n")

new_collector = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto collector for 副业赚钱教程
Uses WP-CLI to publish, with keyword filtering for relevant content.
"""
import feedparser
import subprocess
import time
import re
import os
import json
from datetime import datetime

WP_PATH = "/www/wwwroot/resource_site"
CATEGORY_ID = 53  # 网赚项目
MAX_POSTS = 6
PUBLISHED_FILE = os.path.join(os.path.dirname(__file__), "published.json")
BAIDU_PUSH_URL = "http://data.zz.baidu.com/urls?site=https://www.skillxm.cn&token=zJsDaj5ibt8ZlVgz"

# 副业赚钱相关RSS源
RSS_FEEDS = [
    "https://www.aiyingli.com/feed",      # 爱盈利 - SEO/电商/AI赚钱
    "https://www.woshipm.com/feed",        # 人人都是PM - 产品运营
    "https://www.cyzone.cn/rss/",          # 创业邦 - 创业投资
    "https://sspai.com/feed",              # 少数派 - 效率工具
    "https://www.v2ex.com/index.xml",      # V2EX - 技术副业
]

# 关键词过滤：标题或内容包含这些词才采集
POSITIVE_KEYWORDS = [
    "副业", "赚钱", "网赚", "兼职", "创业", "项目", "教程",
    "变现", "收入", "引流", "私域", "自媒体", "短视频", "直播",
    "电商", "拼多多", "抖音", "闲鱼", "小红书", "公众号",
    "自媒体", "流量", "运营", "SEO", "带货", "知识付费",
    "AI赚钱", "AI变现", "GPT", "ChatGPT", "AIGC",
    "被动收入", "理财", "投资", "基金", "副业项目",
    "接单", "自由职业", "远程", "远程办公",
    "获客", "转化", "成交", "裂变", "社群",
    "模板", "素材", "工具", "资源", "教程",
]

# 排除词：包含这些词的不采集
NEGATIVE_KEYWORDS = [
    "融资", "上市", "IPO", "财报", "裁员", "年报",
    "股价", "市值", "涨停", "跌停", "股市",
    "机器人", "芯片", "半导体", "新能源车",
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
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\\s+', ' ', text)
    return text.strip()

def is_relevant(title, content=""):
    """Check if article is about making money/side hustle"""
    text = (title + " " + content).lower()
    
    # Check negative first
    for kw in NEGATIVE_KEYWORDS:
        if kw in title:
            return False
    
    # Check positive
    for kw in POSITIVE_KEYWORDS:
        if kw in title or kw.lower() in text:
            return True
    
    return False

def wp_post(title, content, cat_id):
    """Publish via WP-CLI"""
    content_file = "/tmp/wp_post_content.txt"
    with open(content_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    
    cmd = (
        'cd %s && '
        'wp post create '
        '--post_type=post '
        '--post_title="%s" '
        '--post_content="$(cat %s)" '
        '--post_category=%d '
        '--post_status=publish '
        '--allow-root 2>&1'
    ) % (WP_PATH, safe_title, content_file, cat_id)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if "Success" in result.stdout:
            m = re.search(r"Created post (\d+)", result.stdout)
            post_id = m.group(1) if m else "?"
            return True, post_id
        else:
            print("  WP Error: %s" % result.stdout[:80])
            return False, ""
    except Exception as e:
        print("  Exception: %s" % str(e))
        return False, ""

def push_to_baidu(urls):
    if not urls:
        return
    try:
        with open("/tmp/baidu_push_urls.txt", "w") as f:
            f.write("\\n".join(urls))
        cmd = 'curl -s --data-binary @/tmp/baidu_push_urls.txt "%s" -H "Content-Type:text/plain" 2>/dev/null' % BAIDU_PUSH_URL
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout.strip():
            print("  Baidu: %s" % result.stdout.strip()[:100])
    except:
        pass

def main():
    print("[%s] Starting collection (副业赚钱)..." % datetime.now().strftime("%Y-%m-%d %H:%M"))
    published = load_published()
    print("  Published cache: %d" % len(published))
    
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
                
                # Keyword filter
                if not is_relevant(title, summary):
                    skipped += 1
                    continue
                
                text = clean_html(summary)
                if len(text) < 80:
                    text = text + "\\n\\n" + link
                
                content = (
                    '<p>%s</p>'
                    '<p>来源: <a href="%s" target="_blank" rel="nofollow">查看原文</a></p>'
                ) % (text, link)
                
                ok, post_id = wp_post(title, content, CATEGORY_ID)
                if ok:
                    published.add(link)
                    new_urls.append("https://www.skillxm.cn/?p=%s" % post_id)
                    total += 1
                    print("  + [%s] %s" % (post_id, title[:35]))
                    time.sleep(2)
                
                if total >= MAX_POSTS:
                    break
        except Exception as e:
            print("    Error: %s" % str(e)[:50])
        
        if total >= MAX_POSTS:
            break
    
    save_published(published)
    
    if new_urls:
        print("\\n  Pushing %d URLs to Baidu..." % len(new_urls))
        push_to_baidu(new_urls)
    
    print("\\n  Result: %d published, %d skipped" % (total, skipped))
    return total

if __name__ == "__main__":
    main()
'''

# Upload
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(new_collector)
sftp.close()
print("1. 采集脚本已更新")

# Clear published cache so it can re-collect
cmd = "echo '[]' > /www/wwwroot/resource_site/auto_collect/published.json"
ssh.exec_command(cmd, timeout=5)
print("2. 已清空发布缓存")

# Test run
print("\n3. 测试运行...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector.py 2>&1",
    timeout=300
)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
