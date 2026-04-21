import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Full theme structure
stdin, stdout, stderr = ssh.exec_command(
    "find /www/wwwroot/resource_site/wp-content/themes/yymarket -type f | head -30",
    timeout=10
)
print('Theme files:\n', stdout.read().decode('utf-8', errors='replace').strip())

# Check functions.php for any login handling
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php",
    timeout=10
)
print('\nfunctions.php:\n', stdout.read().decode('utf-8', errors='replace'))

ssh.close()
