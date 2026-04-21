import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] action/main.php line 150')

# Read around line 150
stdin, stdout, stderr = client.exec_command("sed -n '145,160p' /www/wwwroot/resource_site/wp-content/themes/zibll/action/main.php")
print('Context:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()