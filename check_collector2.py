import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 采集器详细检查 ===\n")

# 1. 检查配置文件
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/config.json", timeout=10)
print("1. 配置文件:")
config = stdout.read().decode().strip()
print(config[:1500] if config else "配置文件为空或不存在")

# 2. 检查数据库
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/auto_collect/*.db 2>/dev/null", timeout=10)
print("\n2. 数据库:")
print(stdout.read().decode().strip() or "无数据库")

# 3. 检查日志目录
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/auto_collect/logs/ 2>/dev/null", timeout=10)
print("\n3. 日志目录:")
print(stdout.read().decode().strip() or "无日志目录")

# 4. 查看最新日志
stdin, stdout, stderr = ssh.exec_command("ls -lt /www/wwwroot/resource_site/auto_collect/logs/ 2>/dev/null | head -5", timeout=10)
print("\n4. 最新日志:")
print(stdout.read().decode().strip() or "无日志")

ssh.close()
