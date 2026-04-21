import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Read footer function
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '46,180p' /www/wwwroot/resource_site/wp-content/themes/yymarket/vessel/login/Login.php",
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
