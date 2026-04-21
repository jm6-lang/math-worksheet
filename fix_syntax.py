import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 直接在服务器上修复那行
fix_cmd = r"""sed -i 's|safe_title = title.replace.*|safe_title = title.replace(chr(92), chr(92)+chr(92)).replace(chr(34), chr(92)+chr(34))|' /www/wwwroot/resource_site/auto_collect/collector.py"""
stdin, stdout, stderr = ssh.exec_command(fix_cmd, timeout=10)

# 测试
print("测试运行...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector.py 2>&1",
    timeout=300
)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
