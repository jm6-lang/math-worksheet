import paramiko
import sys
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 直接从GitHub API搜索蓝天采集器 ===\n")

# 搜索不同的关键词
keywords = ["lantian collector php", "xintein lantian", "lantian scraper"]
for kw in keywords:
    cmd = f"curl -s 'https://api.github.com/search/repositories?q={kw.replace(' ', '+')}&per_page=5' 2>/dev/null"
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    try:
        data = json.loads(stdout.read().decode())
        if data.get('items'):
            print(f"关键词: {kw}")
            for item in data['items'][:3]:
                print(f"  {item.get('html_url')} - {item.get('description', '')[:50]}")
            print()
    except:
        print(f"关键词 {kw}: 无结果")
        print(stdout.read().decode()[:200])

ssh.close()
