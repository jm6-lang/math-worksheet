import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 尝试其他可能的下载地址 ===\n")

# 尝试多个可能的域名
urls = [
    "http://www.lantian.pro",
    "http://lantian.pro",
    "http://www.lantianzz.com", 
    "http://www.lan-tian.com",
    "http://lantian.com",
    "http://www.lansoft.cn",
    "http://www.lantian.net",
]

for url in urls:
    cmd = f'curl -sL --max-time 5 -o /dev/null -w "%{{http_code}}" "{url}" 2>/dev/null'
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    code = stdout.read().decode().strip()
    status = "OK" if code == "200" else code
    print(f"{url}: {status}")

ssh.close()
