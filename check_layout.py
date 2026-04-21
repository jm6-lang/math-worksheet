import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# 1. Check the home page template to understand the layout structure
stdin, stdout, stderr = ssh.exec_command('head -80 /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php', timeout=10)
print('=== home-1.php (first 80 lines) ===')
print(stdout.read().decode('utf-8', errors='replace'))

# 2. Check header.php for the overall layout wrapper
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php | head -50', timeout=10)
print('\n=== header.php (first 50 lines) ===')
print(stdout.read().decode('utf-8', errors='replace'))

# 3. Check footer.php
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php', timeout=10)
print('\n=== footer.php ===')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
