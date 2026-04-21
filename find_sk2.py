import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Search everywhere for sk-custom
stdin, stdout, stderr = client.exec_command(
    'grep -rn "sk-custom\\|wp_enqueue.*sk" /www/wwwroot/ 2>/dev/null | grep -v ".pyc" | head -20',
    timeout=30
)
print('sk-custom search:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
