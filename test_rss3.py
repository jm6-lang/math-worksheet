import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    ("蓝鲸财经", "https://www.lanjinger.com/feed"),
    ("铅笔道", "https://www.pencilnews.cn/feed"),
    ("少数派", "https://sspai.com/feed"),
    ("InfoQ中文", "https://www.infoq.cn/feed"),
    ("爱盈利", "https://www.aiyingli.com/feed"),
    ("V2EX", "https://www.v2ex.com/index.xml"),
    ("财新", "https://rsshub.app/caixin/latest"),
]

for name, url in feeds:
    try:
        f = feedparser.parse(url, request_headers={"User-Agent": "Mozilla/5.0"})
        if f.entries:
            titles = [e.title[:25] for e in f.entries[:3]]
            print("OK [%s] %d | %s" % (name, len(f.entries), " | ".join(titles)))
        else:
            print("NO [%s]" % name)
    except Exception as e:
        print("ERR [%s] %s" % (name, str(e)[:40]))
'''

sftp = ssh.open_sftp()
with sftp.open('/tmp/test_feeds.py', 'w') as f:
    f.write(script)
sftp.close()

print("=== 测试RSS源（副业/赚钱/创业相关）===\n")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/test_feeds.py 2>&1', timeout=180)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
