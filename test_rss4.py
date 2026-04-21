import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

script = '''#!/usr/bin/env python3
import feedparser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

feeds = [
    # RSSHub 二次源 - 知乎副业/赚钱话题
    ("知乎-副业", "https://rsshub.app/zhihu/topics/19551848/hot"),
    ("知乎-网赚", "https://rsshub.app/zhihu/topics/19556289/hot"),
    ("知乎-赚钱", "https://rsshub.app/zhihu/topics/19559991/hot"),
    ("知乎-自媒体", "https://rsshub.app/zhihu/topics/19559990/hot"),
    ("知乎-创业", "https://rsshub.app/zhihu/topics/19551847/hot"),
    ("知乎-副业2", "https://rsshub.app/zhihu/column/c_1374754048728832000"),
    ("微博-创业", "https://rsshub.app/weibo/search?q=副业赚钱"),
    # 其他网赚相关
    ("生财有术", "https://shengcai.info/feed"),
    ("副业君", "https://www.fuyejun.com/feed"),
    ("搞钱", "https://www.gaoqian.com/feed"),
    ("淘客", "https://www.taoke.com/feed"),
    ("自媒体人", "https://www.zimeiti.io/feed"),
    ("流量大师", "https://www.liuliangdash.com/feed"),
    ("创业最前线", "https://www.cyzone.cn/rss/"),
    # 更通用的
    ("掘金", "https://rsshub.app/juejin/trending/weekly/frontend"),
    ("CSDN", "https://rsshub.app/csdn/blog/Python"),
    ("简书-赚钱", "https://rsshub.app/jianshu/trending/weekly"),
    ("豆瓣-副业", "https://rsshub.app/douban/group/690010/explore"),
    ("豆瓣-搞钱", "https://rsshub.app/douban/group/715121/explore"),
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
with sftp.open('/tmp/test_feeds2.py', 'w') as f:
    f.write(script)
sftp.close()

print("=== 测试RSS源（精准副业/网赚）===\n")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/test_feeds2.py 2>&1', timeout=300)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
