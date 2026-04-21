import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 搜索蓝天采集器下载链接 ===\n")

# 尝试不同的域名
domains = [
    "http://www.lantian.pro/lantian",
    "http://www.lantian.pro/download",
    "https://github.com/lantian-project/lantian",
    "https://github.com/lantian-collect/lantian",
]

for domain in domains:
    print(f"尝试: {domain}")
    stdin, stdout, stderr = ssh.exec_command(f"curl -sL --max-time 10 '{domain}' 2>/dev/null | head -c 500", timeout=15)
    content = stdout.read().decode('utf-8', errors='ignore')
    if content and "404" not in content and "Error" not in content[:100]:
        print(f"  找到内容!")
        print(content[:300])
    else:
        print(f"  无内容")
    print()

ssh.close()
