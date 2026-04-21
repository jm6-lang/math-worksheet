import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 查看今天日志的最后部分
print("=== 今天的采集日志 ===\n")
stdin, stdout, stderr = ssh.exec_command("tail -100 /www/wwwroot/resource_site/auto_collect/logs/run_20260407.log", timeout=10)
print(stdout.read().decode().strip())

# 检查cron日志
print("\n\n=== Cron日志 ===\n")
stdin, stdout, stderr = ssh.exec_command("tail -30 /www/wwwroot/resource_site/auto_collect/logs/cron.log", timeout=10)
print(stdout.read().decode().strip())

# 检查数据库记录数
print("\n\n=== 数据库统计 ===\n")
stdin, stdout, stderr = ssh.exec_command("sqlite3 /www/wwwroot/resource_site/auto_collect/published.db 'SELECT COUNT(*) FROM pub; SELECT MAX(created) FROM pub;'", timeout=10)
print(stdout.read().decode().strip())

# 检查定时任务配置
print("\n\n=== 定时任务 ===\n")
stdin, stdout, stderr = ssh.exec_command("crontab -l 2>/dev/null || cat /etc/crontab 2>/dev/null | grep -i collect", timeout=10)
print(stdout.read().decode().strip() or "检查系统cron...")

# 检查系统cron.d
stdin, stdout, stderr = ssh.exec_command("ls -la /etc/cron.d/ 2>/dev/null", timeout=10)
print(stdout.read().decode().strip())

ssh.close()
