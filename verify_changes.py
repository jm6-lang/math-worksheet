import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Check site
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" https://www.skillxm.cn/', timeout=15)
code = stdout.read().decode().strip()
print(f'Site HTTP: {code}')

# Check for syntax errors in PHP
stdin, stdout, stderr = ssh.exec_command('php -l /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php 2>&1', timeout=10)
php_check = stdout.read().decode('utf-8', errors='replace')
print(f'PHP syntax: {php_check.strip()}')

# Count ad slots
stdin, stdout, stderr = ssh.exec_command('grep -c "ad-slot" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php', timeout=10)
ad_count = stdout.read().decode().strip()
print(f'Ad slots in template: {ad_count}')

ssh.close()
