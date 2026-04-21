import paramiko
import sys
import feedparser
import time
import re

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 使用WP-CLI采集发布文章 ===\n")

# RSS源
RSS_FEEDS = [
    {"name": "36kr", "url": "https://www.36kr.com/feed"},
    {"name": "sspai", "url": "https://sspai.com/feed"},
    {"name": "ithome", "url": "https://www.ithome.com/rss/IT"},
]

def clean(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.DOTALL)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.DOTALL)
    t = re.sub(r'<[^>]+>', '', t)
    return t.strip()

def post_wpcli(title, content, cat):
    # 创建临时文件存储内容
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/post_content.txt', 'w') as f:
        f.write(content)
    sftp.close()
    
    # 使用WP-CLI创建文章
    title_esc = title.replace('"', '\\"')
    cmd = f'cd /www/wwwroot/resource_site && wp post create --post_type=post --post_title="{title_esc}" --post_content="$(cat /tmp/post_content.txt)" --post_category={cat} --post_status=publish --allow-root 2>&1'
    
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
    result = stdout.read().decode('utf-8', errors='ignore').strip()
    
    if 'Success' in result or 'created' in result.lower():
        print(f"OK: {title[:30]}...")
        return True
    else:
        print(f"FAIL: {result[:100]}")
        return False

# 开始采集
print("开始采集...\n")
count = 0

for feed in RSS_FEEDS:
    print(f"RSS: {feed['name']}")
    try:
        f = feedparser.parse(feed['url'])
        for entry in f.entries[:2]:
            title = entry.title if hasattr(entry, 'title') else "No Title"
            content = entry.summary if hasattr(entry, 'summary') else entry.title
            content = clean(content)
            if len(content) < 50:
                content = content + "\n\n" + (entry.link if hasattr(entry, 'link') else "")
            content = f"<p>内容整理自网络</p><div>{content}</div><p>来源: {entry.link if hasattr(entry, 'link') else ''}</p>"
            
            if post_wpcli(title, content, 7):  # category 7
                count += 1
                time.sleep(2)
            
            if count >= 6:
                break
        if count >= 6:
            break
    except Exception as e:
        print(f"Error: {str(e)}")
    time.sleep(2)

print(f"\n完成! 共发布 {count} 篇文章")
ssh.close()
