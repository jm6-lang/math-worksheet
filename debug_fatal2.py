import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] Fatal error')

# Get the error
stdin, stdout, stderr = client.exec_command('grep -i "fatal\\|parse" /tmp/test_mu_admin.html 2>/dev/null | head -3')
print('Error:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Check nginx error
stdin, stdout, stderr = client.exec_command('tail -3 /var/log/nginx/error.log')
print('Nginx:', stdout.read().decode('utf-8', errors='ignore').strip()[:600])

client.close()