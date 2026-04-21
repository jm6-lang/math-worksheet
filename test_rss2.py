import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 在服务器上用Python测试，更可靠
script = r'''#!/usr/bin/env python3
import feedparser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

feeds = [
    ("3618med", "https://www.3618med.com/feed"),
    ("虎嗅", "https://www.huxiu.com/rss/0.xml"),
    ("创业邦", "https://www.cyzone.cn/rss/"),
    ("人人都是PM", "https://www.woshipm.com/feed"),
    ("鸟哥笔记", "https://www.niaogebiji.com/feed"),
    ("运营者", "https://www.iyunying.org/feed"),
    ("itbear", "https://www.itbear.com/blog/feed/"),
    ("砍柴网", "https://www.ikanchai.com/feed"),
    ("站长之家", "https://www.chinaz.com/feed"),
    ("A5创业", "https://www.admin5.com/rss.html"),
    ("自媒体", "https://www.zimeiti.com/feed"),
    ("蓝鲸财经", "https://www.lanjinger.com/feed"),
    ("投中网", "https://www.chinaventure.com.cn/rss/"),
    ("铅笔道", "https://www.pencilnews.cn/feed"),
    ("雪球", "https://xueqiu.com/hots/topic/rss"),
    ("少数派", "https://sspai.com/feed"),
    ("InfoQ", "https://www.infoq.cn/feed"),
]

for name, url in feeds:
    try:
        f = feedparser.parse(url, request_headers={'User-Agent': 'Mozilla/5.0'})
        if f.entries:
            titles = [e.title[:30] for e in f.entries[:3]]
            print(f"OK [{name}] {len(f.entries)}条 | {titles}")
        else:
            print(f"NO [{name}] 无内容")
    except Exception as e:
        print(f"ERR [{name}] {str(e)[:50]}")
'''

stdin, stdout, stderr = ssh.exec_command(f'/usr/bin/python3 -c "{script}" 2>&1', timeout=120)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
