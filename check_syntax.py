import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 检查语法错误在哪一行
stdin, stdout, stderr = ssh.exec_command("python3 -c 'import py_compile; py_compile.compile(\"/www/wwwroot/resource_site/auto_collect/collector.py\", doraise=True)' 2>&1", timeout=10)
print("语法检查:", stdout.read().decode().strip() or "语法正确")

# 查看问题行附近
stdin, stdout, stderr = ssh.exec_command("sed -n '135,145p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("\n135-145行:")
print(stdout.read().decode().strip())

ssh.close()
