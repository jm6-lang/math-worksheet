import paramiko
import sys
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 获取蓝天采集器下载信息 ===\n")

# 获取网站内容
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'http://www.lantian.pro' 2>/dev/null", timeout=20)
content = stdout.read().decode('utf-8', errors='ignore')

# 打印所有链接
links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>', content)
print("所有链接:")
for href, text in links[:30]:
    if href.startswith('http') or href.startswith('/'):
        print(f"  {text.strip()}: {href}")

# 查找包含关键词的行
keywords = ['download', '下载', '源码', '开源', 'github', 'php', 'install']
for kw in keywords:
    if kw.lower() in content.lower():
        # 找到附近的文字
        idx = content.lower().find(kw.lower())
        snippet = content[max(0,idx-50):idx+100]
        print(f"\n找到 '{kw}':")
        print(f"  ...{snippet}...")

ssh.close()
