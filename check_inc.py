import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Looking at the require statement')

# Get lines around 91
stdin, stdout, stderr = client.exec_command("sed -n '85,95p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php")
print('Context:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check if this is in the theme version
print('\n[CHECK] Checking theme zip for this file')
stdin, stdout, stderr = client.exec_command('unzip -l /tmp/zibll-7.8.zip | grep -i options-module')
print('In zip:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()