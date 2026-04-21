import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Check the news ticker and search section in home-1.php
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php', timeout=10)
content = stdout.read().decode('utf-8', errors='replace')
print('=== home-1.php full ===')
print(content)

ssh.close()
