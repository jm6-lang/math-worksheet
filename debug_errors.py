import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] Checking for errors')

# Check nginx error log
stdin, stdout, stderr = client.exec_command('tail -30 /var/log/nginx/error.log')
print('Nginx errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Test PHP directly
stdin, stdout, stderr = client.exec_command('SCRIPT_FILENAME=/www/wwwroot/resource_site/index.php REQUEST_METHOD=GET cgi-fcgi -bind -connect unix:/var/run/php/php-fpm.sock 2>/dev/null | head -20')
print('PHP-FPM test:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Test with wget
stdin, stdout, stderr = client.exec_command('wget -qO- --no-check-certificate https://localhost 2>&1 | head -30')
print('wget result:', stdout.read().decode('utf-8', errors='ignore').strip()[:400])

client.close()