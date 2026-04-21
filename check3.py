import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Check collector directory
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/auto_collect/ 2>&1", timeout=10)
print("=== auto_collect 目录 ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check cron log
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/logs/cron.log 2>&1 | tail -50", timeout=10)
print("=== 采集日志 ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check collector.py content
stdin, stdout, stderr = ssh.exec_command("head -80 /www/wwwroot/resource_site/auto_collect/collector.py 2>&1", timeout=10)
print("=== collector.py 前80行 ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
