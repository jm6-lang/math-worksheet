import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 查看完整extract_content函数 ===\n")

# 查看160-280行
stdin, stdout, stderr = ssh.exec_command("sed -n '155,280p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
content = stdout.read().decode()
print(content)

ssh.close()
