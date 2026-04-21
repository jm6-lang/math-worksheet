import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Fresh test')

# Clear nginx error log
stdin, stdout, stderr = client.exec_command('> /var/log/nginx/error.log')

# Make a fresh request
stdin, stdout, stderr = client.exec_command('curl -s -k -H "Host: skillxm.cn" https://127.0.0.1/ 2>&1 | wc -c')
print(f'Homepage bytes: {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Check new errors
time.sleep(1)
stdin, stdout, stderr = client.exec_command('cat /var/log/nginx/error.log')
print(f'New nginx errors: {stdout.read().decode("utf-8", errors="ignore").strip()[:500]}')

# Try the full request with response headers
stdin, stdout, stderr = client.exec_command('curl -v -k -H "Host: skillxm.cn" https://127.0.0.1/ 2>&1 | head -30')
print('Full response:', stdout.read().decode('utf-8', errors='ignore').strip()[:600])

client.close()