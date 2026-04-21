import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 找到函数定义
stdin, stdout, stderr = ssh.exec_command("grep -n '^def mksess\|^def extract_content\|^class WP' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("函数位置:", stdout.read().decode().strip())

# 备份并还原
stdin, stdout, stderr = ssh.exec_command("cp /www/wwwroot/resource_site/auto_collect/collector.py.bak /www/wwwroot/resource_site/auto_collect/collector.py 2>/dev/null || echo '无备份'", timeout=10)
print("还原:", stdout.read().decode().strip())

ssh.close()
