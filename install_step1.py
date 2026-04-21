import paramiko
import sys
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 完成天空采集器安装向导 ===\n")

# Step 1: 接受许可协议
print("1. 接受许可协议...")
cmd = """curl -sL 'http://caiji.skillxm.cn/index.php?s=/install/index/step1' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')

# 查找下一步链接
step2 = re.search(r'href="(/index\.php\?s=/[^"]*step2[^"]*)"', content)
step1_content = re.search(r'href="(/index\.php\?s=/install/index/step1[^"]*)"', content)
print("   内容:", content[:500] if content else "空")
if step2:
    next_url = step2.group(1)
    print(f"   下一步: {next_url}")
elif step1_content:
    next_url = step1_content.group(1)
    print(f"   链接: {next_url}")
else:
    print("   未找到下一步链接")
    print("   完整内容:", content[:1000])

ssh.close()
