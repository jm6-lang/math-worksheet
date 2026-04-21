import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check the skillxm_custom_styles function and fun-custom.php
stdin, stdout, stderr = client.exec_command(
    'grep -n "skillxm_custom_styles\\|fun-custom" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php | head -10',
    timeout=10
)
print('skillxm_custom_styles:')
print(stdout.read().decode('utf-8', errors='replace'))

# Check fun-custom.php
stdin, stdout, stderr = client.exec_command(
    'cat /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/fun-custom.php 2>/dev/null | head -30',
    timeout=10
)
print('\nfun-custom.php:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
