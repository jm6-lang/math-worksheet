import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Check if zibll.com is the issue')

# Test DNS resolution for zibll.com
stdin, stdout, stderr = client.exec_command('timeout 5 nslookup zibll.com 2>&1')
dns = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'DNS zibll.com: {dns[:300]}')

# Test connecting to zibll.com
stdin, stdout, stderr = client.exec_command('timeout 5 curl -s -o /dev/null -w "%{http_code}" https://zibll.com 2>&1')
zibll = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'zibll.com HTTP: {zibll}')

# Test if the theme is the issue - temporarily switch to default theme
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'twentytwentyfour' WHERE option_name IN ('template', 'stylesheet', 'current_theme');\"")
print('Switched to default theme')

# Restart and test
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')
time.sleep(2)

stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | wc -c')
size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage with default theme: {size} bytes')

stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -5')
page = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Page: {page[:300]}')

client.close()