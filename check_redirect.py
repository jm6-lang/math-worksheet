import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Nginx redirect source')

# Check for 301 redirects in nginx
stdin, stdout, stderr = client.exec_command('grep -r "return 301" /etc/nginx/')
print('301 redirects:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check conf.d
stdin, stdout, stderr = client.exec_command('ls -la /etc/nginx/conf.d/')
print('Conf.d files:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()