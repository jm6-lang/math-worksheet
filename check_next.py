import paramiko
import sys
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查 next.lantian.pro ===\n")

# 获取页面
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'https://next.lantian.pro/' 2>/dev/null | head -c 3000", timeout=20)
content = stdout.read().decode('utf-8', errors='ignore')
print("next.lantian.pro内容:")
print(content[:2000])

# 查找下载链接
print("\n\n下载链接:")
links = re.findall(r'href=["\']([^"\']*(?:download|zip|github|release|install)[^"\']*)["\']', content, re.I)
for l in links[:10]:
    print(f"  {l}")

ssh.close()
