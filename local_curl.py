import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Direct curl from server to itself
stdin, stdout, stderr = client.exec_command(
    'curl -s "http://127.0.0.1/" 2>&1 | grep -i "custom" | head -5',
    timeout=15
)
print('Direct server curl:')
print(stdout.read().decode('utf-8', errors='replace'))

# Check for CDN/Proxy headers
stdin, stdout, stderr = client.exec_command(
    'curl -sI "http://127.0.0.1/" 2>&1 | grep -i "cdn\\|via\\|x-cache\\|server\\|cloud"',
    timeout=10
)
print('\nHeaders:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
