import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Test PHP-FPM output')

# Create test.php properly
stdin, stdout, stderr = client.exec_command('printf "<?php\\nheader(\"Content-Type: text/plain\");\\necho \"HELLO\";\\n?>" > /www/wwwroot/resource_site/test.php')
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/test.php')
print('test.php content:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/test.php')
stdin, stdout, stderr = client.exec_command('chmod 644 /www/wwwroot/resource_site/test.php')

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 5 https://127.0.0.1/test.php 2>&1')
test_result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Test page result: "{test_result}" (length: {len(test_result)})')

# Also try HTTP (not HTTPS)
stdin, stdout, stderr = client.exec_command('curl -s --max-time 5 http://127.0.0.1/test.php 2>&1')
test_http = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Test HTTP result: "{test_http}" (length: {len(test_http)})')

# Check nginx access log for the request
stdin, stdout, stderr = client.exec_command('tail -3 /var/log/nginx/access.log')
print('Access log:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()