import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Fix wp-config.php')

# Restore from backup
stdin, stdout, stderr = client.exec_command('cp /tmp/wp_config_backup /www/wwwroot/resource_site/wp-config.php 2>/dev/null')
print(f'Restore: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check if backup exists
stdin, stdout, stderr = client.exec_command('ls -la /tmp/wp_config_backup 2>/dev/null')
backup = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Backup: {backup}')

# If no backup, fix manually by putting the PHP tag back first
if 'No such' in backup:
    # Move the ini_set line after the opening PHP tag
    stdin, stdout, stderr = client.exec_command("sed -i '1d' /www/wwwroot/resource_site/wp-config.php")
    # Now first line should be <?php
    # Insert after first line
    stdin, stdout, stderr = client.exec_command("sed -i '1a ini_set(\"display_errors\", 1); ini_set(\"display_startup_errors\", 1); error_reporting(E_ALL);' /www/wwwroot/resource_site/wp-config.php")
    print('Fixed manually')
else:
    # Add debug lines properly after <?php
    stdin, stdout, stderr = client.exec_command("sed -i '2i ini_set(\"display_errors\", 1); ini_set(\"display_startup_errors\", 1); error_reporting(E_ALL);' /www/wwwroot/resource_site/wp-config.php")
    print('Inserted after line 1')

# Verify
stdin, stdout, stderr = client.exec_command('head -5 /www/wwwroot/resource_site/wp-config.php')
print('Top:', stdout.read().decode('utf-8', errors='ignore').strip())

# Syntax check
stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-config.php 2>&1')
print('Syntax:', stdout.read().decode('utf-8', errors='ignore').strip())

# Restart PHP
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')
time.sleep(2)

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | wc -c')
size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage bytes: {size}')

stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -5')
print('Homepage:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

client.close()