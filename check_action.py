import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] All zibpay references')

# Find all zibpay references in action folder
stdin, stdout, stderr = client.exec_command('grep -r "zibpay" /www/wwwroot/resource_site/wp-content/themes/zibll/action/ 2>/dev/null | head -20')
print('Action zibpay:', stdout.read().decode('utf-8', errors='ignore').strip()[:600])

client.close()