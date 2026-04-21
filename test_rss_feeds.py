import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 测试可用的RSS源 ===\n")

# 测试不同的中文RSS源
rss_feeds = [
    ("创业邦", "https://www.cyzone.cn/rss/"),
    ("虎嗅", "https://www.huxiu.com/rss/"),
    ("少数派", "https://sspai.com/feed"),
    ("CSDN", "https://blog.csdn.net/rss/rss_list?channel=ALL"),
    ("博客园", "https://feed.cnblogs.com/blog/sitefeed/rss"),
    ("知乎日报", "https://rsshub.app/zhihu/daily"),
    ("腾讯新闻", "https://news.qq.com/rss/news.xml"),
]

for name, url in rss_feeds:
    cmd = f'curl -sL --max-time 10 "{url}" | head -c 500'
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    result = stdout.read().decode('utf-8', errors='ignore')[:200]
    status = "OK" if "<rss" in result or "<feed" in result or len(result) > 100 else "Failed"
    print(f"{name}: {status}")
    if status == "OK":
        print(f"   Preview: {result[:150]}...")
    print()

ssh.close()
