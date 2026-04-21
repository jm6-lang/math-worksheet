import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查内容提取工具 ===\n")

# 1. 检查trafilatura
stdin, stdout, stderr = ssh.exec_command("pip3 show trafilatura 2>/dev/null || echo '未安装'", timeout=10)
print("1. Trafilatura:", stdout.read().decode().strip())

# 2. 检查其他提取工具
stdin, stdout, stderr = ssh.exec_command("pip3 list 2>/dev/null | grep -iE 'beautifulsoup|requests|selenium|playwright|newspaper'", timeout=10)
print("\n2. 可用库:")
print(stdout.read().decode().strip() or "无")

# 3. 测试requests+BeautifulSoup提取
print("\n3. 测试内容提取...")
cmd = 'python3 -c "import requests; from bs4 import BeautifulSoup; r = requests.get(\\\'https://www.36kr.com/\\\', headers={\\\'User-Agent\\\': \\\'Mozilla/5.0\\\'}, timeout=10); print(\\\'Status:\\\", r.status_code, \\\'Len:\\\", len(r.text))"'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
print(stdout.read().decode().strip())

# 4. 测试百度搜索是否可用
print("\n4. 测试搜索API...")
cmd = 'curl -s "https://www.baidu.com/s?wd=test&rn=5" -H "User-Agent: Mozilla/5.0" | head -c 500'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
result = stdout.read().decode().strip()
print("百度搜索:", "正常" if "test" in result else "被限制")

ssh.close()
