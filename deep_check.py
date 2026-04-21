import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 深入诊断 ===\n")

# 1. 采集日志内容
print("1. 采集脚本日志内容:")
cmd = "cat /www/wwwroot/resource_site/auto_collect/logs/cron.log 2>/dev/null | tail -50"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
log = stdout.read().decode('utf-8', errors='ignore').strip()
print(log[-2000:] if log else "日志为空!")

# 2. 采集脚本配置
print("\n2. 采集脚本配置:")
cmd = "cat /www/wwwroot/resource_site/auto_collect/config.json 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 3. 手动运行采集脚本
print("\n3. 手动运行采集脚本测试:")
cmd = "cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector.py 2>&1 | tail -30"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
print(stdout.read().decode('utf-8', errors='ignore').strip()[-1500:])

ssh.close()
