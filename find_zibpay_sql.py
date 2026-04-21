import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Zibpay install/sql files')

# Find SQL or install files in zibpay
stdin, stdout, stderr = client.exec_command('find /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/ -name "*.sql" 2>/dev/null')
print('SQL files:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('find /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/ -name "*install*" -o -name "*activate*" -o -name "*create*table*" 2>/dev/null')
print('Install files:', stdout.read().decode('utf-8', errors='ignore').strip())

# List all files in zibpay.disabled recursively
stdin, stdout, stderr = client.exec_command('find /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/ -type f 2>/dev/null')
print('All files:', stdout.read().decode('utf-8', errors='ignore').strip()[:800])

client.close()
print('[DONE]')