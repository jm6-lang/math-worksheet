import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 测试网络连接 ===\n")

# 测试基本连接
tests = [
    ("Google", "https://www.google.com"),
    ("Baidu", "https://www.baidu.com"),
    ("36kr", "https://36kr.com"),
    ("RSSHub", "https://rsshub.app"),
    ("RSSHub IT", "https://rsshub.app/ithome/ranking/daily"),
]

for name, url in tests:
    cmd = f'curl -sL -o /dev/null -w "%{{http_code}}" --max-time 10 "{url}"'
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    code = stdout.read().decode().strip()
    print(f"{name}: {code}")

ssh.close()
