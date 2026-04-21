import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Zibpay all files')

# List ALL files
stdin, stdout, stderr = client.exec_command('find /www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/ -type f 2>/dev/null')
all_files = stdout.read().decode('utf-8', errors='ignore').strip()
print('All zibpay files:')
for f in all_files.split('\n'):
    print(f'  {f}')

client.close()