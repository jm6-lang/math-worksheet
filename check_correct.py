import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Find the enqueue area in the correct functions.php
stdin, stdout, stderr = client.exec_command(
    'grep -n "pk_init_wp_empty_style\\|wp_enqueue_style.*puock\\|add_action.*wp_enqueue" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php | head -10',
    timeout=10
)
print('Enqueue area:')
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

# Also check around line 628 like before
stdin, stdout, stderr = client.exec_command(
    'sed -n "620,640p" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php',
    timeout=10
)
print('Lines 620-640:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
