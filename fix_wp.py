import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Fixing wp-config.php')

# Read current wp-config
stdin, stdout, stderr = client.exec_command('cat /www/wwwroot/resource_site/wp-config.php')
content = stdout.read().decode('utf-8', errors='ignore')

# Print first 20 lines to see the issue
print('Current content lines 1-20:')
for i, line in enumerate(content.split('\n')[:20], 1):
    print(f'{i}: {line}')

# Fix the missing variable - find the broken line and fix it
lines = content.split('\n')
fixed_lines = []
for line in lines:
    if " = 'wp_';" in line and '$table_prefix' not in line:
        fixed_lines.append("$table_prefix = 'wp_';")
    else:
        fixed_lines.append(line)

fixed_content = '\n'.join(fixed_lines)

# Write back
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-config.php', 'w')
f.write(fixed_content)
f.close()

print('[FIXED] wp-config.php')

# Now try wp-cli again
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && wp theme activate zibll --allow-root 2>&1')
print('WP-CLI result:', stdout.read().decode('utf-8', errors='ignore').strip())

# Verify activation
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT option_value FROM wp_resource.wp_options WHERE option_name = \\"template\\";" 2>/dev/null')
print('Template after:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE]')