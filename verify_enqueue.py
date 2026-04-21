import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Check the enqueue line in functions.php
stdin, stdout, stderr = client.exec_command(
    'grep -n "sk-custom\\|custom.css\\|assets/custom" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php',
    timeout=10
)
content = stdout.read().decode('utf-8', errors='replace').strip()
print('Enqueue line:', content)

# Also check if the file is properly readable
stdin, stdout, stderr = client.exec_command(
    'head -5 /www/wwwroot/resource_site/wp-content/themes/puock/assets/custom.css',
    timeout=10
)
print('CSS file content:')
print(stdout.read().decode('utf-8', errors='replace'))

# Check what the theme's main style URL looks like
stdin, stdout, stderr = client.exec_command(
    'grep -n "get_stylesheet_uri\\|get_template_directory_uri" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php | head -5',
    timeout=10
)
print('Style URI lines:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
