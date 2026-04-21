import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 查找蓝天采集器 ===\n")

# 查找是否已安装
stdin, stdout, stderr = ssh.exec_command("find /www/wwwroot -name '*lantian*' -o -name '*lancms*' 2>/dev/null | head -10", timeout=15)
print("已安装的蓝天相关文件:")
print(stdout.read().decode().strip() or "无\n")

# 查找网站目录
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/", timeout=10)
print("\n网站目录:")
print(stdout.read().decode().strip())

# 检查是否在子目录
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/ | head -20", timeout=10)
print("\nresource_site目录:")
print(stdout.read().decode().strip())

ssh.close()
