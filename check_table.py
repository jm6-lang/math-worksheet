import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
stdin, stdout, stderr = ssh.exec_command("mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e 'DESCRIBE wp_posts'", timeout=30)
print(stdout.read().decode('utf-8'))
ssh.close()
