import paramiko
import sys
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 测试GitHub API ===\n")

# 测试基本的GitHub API
cmd = "curl -s 'https://api.github.com/repos/torvalds/linux' 2>/dev/null | head -c 500"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("测试linux repo:")
print(stdout.read().decode()[:300])

# 搜索采集器
print("\n搜索PHP采集器:")
cmd = "curl -s 'https://api.github.com/search/repositories?q=web+scraper+php&per_page=5' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
try:
    data = json.loads(stdout.read().decode())
    print(f"找到 {data.get('total_count', 0)} 个结果")
    for item in data.get('items', [])[:3]:
        print(f"  {item.get('html_url')}")
except Exception as e:
    print(f"错误: {e}")
    print(stdout.read().decode()[:200])

ssh.close()
