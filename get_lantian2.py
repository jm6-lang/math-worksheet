import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

print("=== 获取蓝天采集器信息 ===\n")

# 获取网站内容
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'http://www.lantian.pro' 2>/dev/null | head -c 3000", timeout=20)
content = stdout.read().decode('utf-8', errors='ignore')
print(content[:2000])

ssh.close()
