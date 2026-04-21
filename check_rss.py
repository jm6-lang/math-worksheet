import paramiko
import feedparser

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查RSS源内容 ===\n")

# 检查不同RSS源
rss_feeds = [
    "https://www.36kr.com/feed",
    "https://sspai.com/feed",
    "https://www.admin5.com/rss/",
]

for feed_url in rss_feeds:
    print(f"=== {feed_url} ===")
    cmd = f'curl -s "{feed_url}" | head -c 3000'
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    content = stdout.read().decode('utf-8', errors='ignore')
    print(content[:1500])
    print("\n")

ssh.close()
