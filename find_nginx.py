import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')
stdin, stdout, stderr = ssh.exec_command("find /www -name '*.conf' 2>/dev/null | grep -i skillxm | head -10", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
stdin, stdout, stderr = ssh.exec_command("ls /www/server/panel/vhost/nginx/ 2>/dev/null | head -20", timeout=15)
print(stdout.read().decode('utf-8', errors='replace'))
ssh.close()
