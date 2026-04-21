import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Verify what's actually in skillxm functions.php line 631 area
stdin, stdout, stderr = client.exec_command(
    'sed -n "628,640p" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('skillxm functions.php 628-640:')
print(stdout.read().decode('utf-8', errors='replace'))

# Also check line 761-765
stdin, stdout, stderr = client.exec_command(
    'sed -n "758,766p" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('\nskillxm functions.php 758-766:')
print(stdout.read().decode('utf-8', errors='replace'))

# Directly check what wp_enqueue_style calls are in skillxm's functions.php
stdin, stdout, stderr = client.exec_command(
    'grep -n "wp_enqueue_style" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('\nAll wp_enqueue_style in skillxm:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
