import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 查看函数位置 ===\n")

# 查找WordPress类位置（函数在它之前）
stdin, stdout, stderr = ssh.exec_command("grep -n 'class WP' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("WordPress类:", stdout.read().decode().strip())

# 查找函数
stdin, stdout, stderr = ssh.exec_command("grep -n 'def extract_content\\|def mksess' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("函数:", stdout.read().decode().strip())

# 查看140-165行
stdin, stdout, stderr = ssh.exec_command("sed -n '140,165p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("\n140-165行:")
print(stdout.read().decode().strip())

ssh.close()
