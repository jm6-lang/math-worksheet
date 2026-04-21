import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check wp-config.php
stdin, stdout, stderr = client.exec_command(
    'cat /www/wwwroot/skillxm.cn/public/wp-config.php | grep -v "^//\|^#\|password\|secret\|key" | head -40',
    timeout=10
)
print('wp-config.php:')
print(stdout.read().decode('utf-8', errors='replace'))

# Also check if there's ABSPATH defined
stdin, stdout, stderr = client.exec_command(
    'grep -n "ABSPATH\\|WP_CONTENT_DIR\\|WP_PLUGIN_DIR" /www/wwwroot/skillxm.cn/public/wp-config.php',
    timeout=10
)
print('\nABSPATH:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
