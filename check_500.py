import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Recent 500 errors')

# Get recent errors
stdin, stdout, stderr = client.exec_command('tail -100 /var/log/nginx/error.log 2>/dev/null | tail -50')
print('Recent errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:1000])

client.close()