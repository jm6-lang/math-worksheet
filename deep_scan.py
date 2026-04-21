import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('=== Files with gzinflate ===')
stdin, stdout, stderr = client.exec_command('grep -rl "gzinflate" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null')
print(stdout.read().decode('utf-8', errors='ignore'))

print('\n=== go.php suspicious checks ===')
stdin, stdout, stderr = client.exec_command('grep -c "eval" /www/wwwroot/resource_site/wp-content/themes/zibll/go.php')
print('eval count:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('grep -c "base64_decode" /www/wwwroot/resource_site/wp-content/themes/zibll/go.php')
print('base64_decode count:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('grep -c "shell_exec" /www/wwwroot/resource_site/wp-content/themes/zibll/go.php')
print('shell_exec count:', stdout.read().decode('utf-8', errors='ignore').strip())

print('\n=== go.php first 50 lines ===')
stdin, stdout, stderr = client.exec_command('head -50 /www/wwwroot/resource_site/wp-content/themes/zibll/go.php')
print(stdout.read().decode('utf-8', errors='ignore'))

print('\n=== header.php suspicious check ===')
stdin, stdout, stderr = client.exec_command('grep -c "eval" /www/wwwroot/resource_site/wp-content/themes/zibll/header.php')
print('header.php eval count:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('grep -c "gzinflate" /www/wwwroot/resource_site/wp-content/themes/zibll/header.php')
print('header.php gzinflate count:', stdout.read().decode('utf-8', errors='ignore').strip())

print('\n=== Check qrcode.class.php ===')
stdin, stdout, stderr = client.exec_command('ls -la /www/wwwroot/resource_site/wp-content/themes/zibll/inc/class/qrcode.class.php')
print(stdout.read().decode('utf-8', errors='ignore'))

stdin, stdout, stderr = client.exec_command('wc -c /www/wwwroot/resource_site/wp-content/themes/zibll/inc/class/qrcode.class.php')
print('qrcode.class.php size:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('\n[DONE]')