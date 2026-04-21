import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] PHP-FPM configuration')

# Check PHP-FPM pool config
stdin, stdout, stderr = client.exec_command('cat /etc/php/8.1/fpm/pool.d/www.conf 2>/dev/null | grep -E "php_admin|php_value|output_buffer|display_errors|error_log"')
print('Pool config:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check php.ini for output_buffering
stdin, stdout, stderr = client.exec_command('php -i 2>/dev/null | grep -i "output_buffering\\|display_errors\\|error_log\\|error_reporting"')
print('PHP info:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check the actual FPM php.ini (might be different from CLI)
stdin, stdout, stderr = client.exec_command('php-fpm8.1 -i 2>/dev/null | grep -i "output_buffering\\|display_errors\\|error_log"')
print('FPM php info:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Test PHP-FPM directly via the socket
stdin, stdout, stderr = client.exec_command('SCRIPT_NAME=/test.php SCRIPT_FILENAME=/www/wwwroot/resource_site/test.php REQUEST_METHOD=GET cgi-fcgi -bind -connect /run/php/php-fpm.sock 2>&1')
print('Direct FPM test:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check if test.php exists
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/test.php 2>/dev/null')
print('test.php:', stdout.read().decode('utf-8', errors='ignore').strip())

# Create test.php again
stdin, stdout, stderr = client.exec_command('echo "<?php header(\"Content-Type: text/plain\"); echo \"HELLO WORLD\"; ?>" > /www/wwwroot/resource_site/test.php')
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/test.php')

# Try curl again
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 5 https://127.0.0.1/test.php 2>&1')
print('Test page:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check nginx config for .php handling
stdin, stdout, stderr = client.exec_command('nginx -T 2>/dev/null | grep -A 10 "location.*\\.php"')
print('Nginx PHP config:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()