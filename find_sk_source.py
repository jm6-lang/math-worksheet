import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check if there's already a custom.css in puock/assets/ 
stdin, stdout, stderr = client.exec_command(
    'ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/custom.css',
    timeout=10
)
print('custom.css in puock/assets/:')
print(stdout.read().decode('utf-8', errors='replace'))

# Also check if there's an index.php in assets that might be redirecting
stdin, stdout, stderr = client.exec_command(
    'ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/',
    timeout=10
)
print('\npuock/assets/ dir:')
print(stdout.read().decode('utf-8', errors='replace'))

# Search for sk-custom-css ID source again but more carefully
stdin, stdout, stderr = client.exec_command(
    'grep -rn "sk-custom-css" /www/wwwroot/skillxm.cn/public/ 2>/dev/null',
    timeout=30
)
print('\nsk-custom-css sources:')
out = stdout.read().decode('utf-8', errors='replace')
print(out if out.strip() else "(not found)")

client.close()
