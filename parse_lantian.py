import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 访问蓝天采集器官网 ===\n")

# 获取完整页面并查找下载链接
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'http://www.lantian.pro' 2>/dev/null", timeout=20)
content = stdout.read().decode('utf-8', errors='ignore')

# 查找下载相关链接
import re
downloads = re.findall(r'href=["\']([^"\']*(?:download|zip|tar|release|github)[^"\']*)["\']', content, re.I)
print("下载相关链接:")
for d in downloads[:10]:
    print(f"  {d}")

# 查找GitHub链接
github = re.findall(r'href=["\'](https?://github\.com/[^"\']+)["\']', content)
print("\nGitHub链接:")
for g in github[:10]:
    print(f"  {g}")

# 查找开源相关文字
opensource = re.findall(r'开源|github|源码|download|php|python', content, re.I)
print(f"\n开源相关词出现次数: {len(opensource)}")

ssh.close()
