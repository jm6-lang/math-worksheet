import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[DEBUG] Check actual response content')

# Get the actual full response including headers
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 -D - https://127.0.0.1/ 2>&1')
response = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Full response ({len(response)} bytes):')
print(response[:1000])

# Also check wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 -D - https://127.0.0.1/wp-admin/ 2>&1')
response2 = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'\nAdmin response ({len(response2)} bytes):')
print(response2[:1000])

client.close()