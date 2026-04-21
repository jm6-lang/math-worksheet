import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Find where skillxm.cn WordPress is installed
stdin, stdout, stderr = client.exec_command(
    'find /www -name "wp-config.php" 2>/dev/null | head -10',
    timeout=15
)
print('WP installs:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
