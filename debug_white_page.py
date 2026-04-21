import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] White page error')

# Check PHP error log
stdin, stdout, stderr = client.exec_command('tail -20 /var/log/php8.1-fpm.log')
print('PHP log:', stdout.read().decode('utf-8', errors='ignore').strip()[:800])

# Check nginx error
stdin, stdout, stderr = client.exec_command('tail -10 /var/log/nginx/error.log')
print('Nginx log:', stdout.read().decode('utf-8', errors='ignore').strip()[:800])

# Get actual page content with errors
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | head -50')
page = stdout.read().decode('utf-8', errors='ignore')
print('Page start:', page[:500])

# Check if there's a fatal error hidden
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | grep -i "fatal\\|error\\|parse" | head -5')
print('Errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check PHP display_errors setting
stdin, stdout, stderr = client.exec_command('php -r "echo ini_get(\'display_errors\');"')
print('display_errors:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check wp-config for debug
stdin, stdout, stderr = client.exec_command('grep -i "debug\\|error" /www/wwwroot/resource_site/wp-config.php | head -5')
print('WP debug:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()