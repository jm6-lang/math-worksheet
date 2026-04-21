import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check if skillxm's puock theme is symlinked to resource_site
stdin, stdout, stderr = client.exec_command(
    'ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/puock | head -5',
    timeout=10
)
print('skillxm puock dir:')
print(stdout.read().decode('utf-8', errors='replace'))

# Get inode numbers to see if they're the same
stdin, stdout, stderr = client.exec_command(
    'stat /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php /www/wwwroot/resource_site/wp-content/themes/puock/functions.php 2>/dev/null | grep -E "Inode|File"',
    timeout=10
)
print('\nInode comparison:')
print(stdout.read().decode('utf-8', errors='replace'))

# Realpath of the skillxm puock functions.php
stdin, stdout, stderr = client.exec_command(
    'realpath /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('\nRealpath:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
