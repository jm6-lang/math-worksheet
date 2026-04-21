import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Read full home-1.php
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php', timeout=10)
home1 = stdout.read().decode('utf-8', errors='replace')

# Read full archive.php
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/archive.php', timeout=10)
archive = stdout.read().decode('utf-8', errors='replace')

# Read full index.php
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/index.php', timeout=10)
indexphp = stdout.read().decode('utf-8', errors='replace')

print('=== home-1.php ===')
print(home1)
print('\n\n=== archive.php ===')
print(archive)
print('\n\n=== index.php ===')
print(indexphp)

ssh.close()
