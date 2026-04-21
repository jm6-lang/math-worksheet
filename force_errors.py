import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Force display errors')

# Add error display at the very TOP of wp-config.php, before everything else
stdin, stdout, stderr = client.exec_command("head -3 /www/wwwroot/resource_site/wp-config.php")
print('Current top:', stdout.read().decode('utf-8', errors='ignore').strip())

# Insert ini_set at the very beginning
stdin, stdout, stderr = client.exec_command("sed -i '1i ini_set(\"display_errors\", 1); ini_set(\"display_startup_errors\", 1); error_reporting(E_ALL);' /www/wwwroot/resource_site/wp-config.php")

# Verify
stdin, stdout, stderr = client.exec_command('head -5 /www/wwwroot/resource_site/wp-config.php')
print('After:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check syntax
stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-config.php 2>&1')
print('Syntax:', stdout.read().decode('utf-8', errors='ignore').strip())

# Restart PHP
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')

import time
time.sleep(2)

# Test again
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1')
page = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage ({len(page)} chars):')
print(page[:1000] if page else 'EMPTY')

client.close()