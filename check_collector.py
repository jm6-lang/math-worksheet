import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 采集器状态检查 ===\n")

# 1. 检查采集器文件
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/auto_collect/", timeout=10)
print("1. 采集器目录:")
print(stdout.read().decode().strip())

# 2. 检查采集器进程
stdin, stdout, stderr = ssh.exec_command("ps aux | grep -i collect | grep -v grep", timeout=10)
print("\n2. 采集器进程:")
print(stdout.read().decode().strip() or "无运行中的进程")

# 3. 检查定时任务
stdin, stdout, stderr = ssh.exec_command("crontab -l 2>/dev/null", timeout=10)
print("\n3. 定时任务:")
cron = stdout.read().decode().strip()
print(cron or "无定时任务")

# 4. 检查systemd服务
stdin, stdout, stderr = ssh.exec_command("systemctl list-units --type=service | grep -i collect", timeout=10)
print("\n4. Systemd服务:")
print(stdout.read().decode().strip() or "无采集器服务")

# 5. 检查日志
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/auto_collect/*.log 2>/dev/null || echo '无日志文件'", timeout=10)
print("\n5. 日志文件:")
print(stdout.read().decode().strip())

# 6. 查看最近日志
stdin, stdout, stderr = ssh.exec_command("tail -50 /www/wwwroot/resource_site/auto_collect/collector.log 2>/dev/null || tail -50 /www/wwwroot/resource_site/auto_collect/*.log 2>/dev/null || echo '无日志可查看'", timeout=15)
print("\n6. 最近日志:")
print(stdout.read().decode().strip()[:1000])

# 7. 检查采集器配置
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/collector.py | head -50", timeout=10)
print("\n7. 采集器配置（前50行）:")
print(stdout.read().decode().strip())

ssh.close()
