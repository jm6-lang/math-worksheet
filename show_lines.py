import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 查看135-200行
stdin, stdout, stderr = ssh.exec_command("sed -n '135,200p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("135-200行:")
print(stdout.read().decode().strip())

ssh.close()
