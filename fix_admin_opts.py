import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Comment out ZibAut::is_update() call')

# Read admin-options.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

# Replace the problematic line
old_line = '    $is_update_data = ZibAut::is_update();'
new_line = '    $is_update_data = null; // disabled: ZibAut::is_update();'

if old_line in content:
    content = content.replace(old_line, new_line, 1)
    print('Replaced is_update call')
else:
    print('Line not found, trying line number approach')
    lines = content.split('\n')
    if 'ZibAut::is_update()' in lines[11089]:
        lines[11089] = new_line
        content = '\n'.join(lines)
        print('Replaced at line 11090')

# Write back
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', 'w')
f.write(content)
f.close()

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php')
print('Fixed permissions')

# Test
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')
stdin, stdout, stderr = client.exec_command('sleep 1 && curl -s -k "https://127.0.0.1/wp-admin/" -o /tmp/test_final_admin.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin HTTP: {admin_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal" /tmp/test_final_admin.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors: {fatal}')

# Homepage
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/" -o /dev/null -w "%{http_code}" 2>&1')
home = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage HTTP: {home}')

# Registration
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php?action=register" -o /dev/null -w "%{http_code}" 2>&1')
reg = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Registration HTTP: {reg}')

client.close()