import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Search EVERYTHING for sk-custom-css
stdin, stdout, stderr = client.exec_command(
    'grep -rn "sk-custom" /www/wwwroot/ 2>/dev/null | grep -v "Binary\\|node_modules" | grep -v ".pyc" | head -30',
    timeout=30
)
print('All sk-custom refs:')
for line in stdout.read().decode('utf-8', errors='replace').strip().split('\n'):
    print(line)

# Also check if there are any WP plugins that might inject CSS
stdin, stdout, stderr = client.exec_command(
    'grep -rn "sk-custom\\|custom.css.*ver" /www/wwwroot/skillxm.cn/public/wp-content/plugins/ 2>/dev/null | head -10',
    timeout=30
)
print('\nPlugin refs:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
