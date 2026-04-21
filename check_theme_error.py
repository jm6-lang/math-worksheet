import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# First check the syntax error in functions.php line 268
stdin, stdout, stderr = ssh.exec_command("sed -n '260,275p' /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php")
print("functions.php lines 260-275:", flush=True)
print(stdout.read().decode('utf-8', errors='replace'), flush=True)

ssh.close()
