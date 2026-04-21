import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Find sk-custom-css or custom.css in all PHP files under skillxm
stdin, stdout, stderr = client.exec_command(
    'grep -rn "sk-custom-css\\|assets/custom.css" /www/wwwroot/skillxm.cn/public/ 2>/dev/null | head -20',
    timeout=30
)
print('sk-custom-css references:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
