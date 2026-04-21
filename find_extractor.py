import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 找到extract_content函数
print("=== 查找extract_content函数 ===\n")
stdin, stdout, stderr = ssh.exec_command("grep -n 'def extract_content' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("extract_content定义位置:", stdout.read().decode().strip())

# 查看这个函数
stdin, stdout, stderr = ssh.exec_command("sed -n '160,220p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("\n函数内容:")
print(stdout.read().decode().strip())

# 查看调用extract_content的地方
print("\n\n=== 调用extract_content的地方 ===")
stdin, stdout, stderr = ssh.exec_command("grep -n 'extract_content' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print(stdout.read().decode().strip())

ssh.close()
