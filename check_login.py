import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check login modal template
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/vessel/login/templates/modal.php",
    timeout=10
)
modal = stdout.read().decode('utf-8', errors='replace')
print('Modal template (first 2000 chars):\n', modal[:2000])

# Check login script
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/vessel/login/static/js/script.js",
    timeout=10
)
js = stdout.read().decode('utf-8', errors='replace')
print('\nLogin JS (first 1500 chars):\n', js[:1500])

ssh.close()
