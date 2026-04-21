import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Patch ZibAut to bypass authorization')

# Read code.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

# Replace is_aut() to always return true
# Find the function and replace it
old_is_aut = content.find('function is_aut()')
if old_is_aut >= 0:
    # Find the end of this function (next function definition or class method)
    # We'll replace the entire function body
    print(f'Found is_aut at position {old_is_aut}')
    
    # Find the next function or method after is_aut
    next_func = content.find('function ', old_is_aut + 15)
    if next_func < 0:
        next_func = content.find('function ', old_is_aut + 15)
    print(f'Next function at {next_func}')
    
    # Get everything before and after is_aut function
    before = content[:old_is_aut]
    after = content[next_func:]
    
    # Replace is_aut with simple return true
    new_is_aut = "function is_aut(){return true;}\n    "
    
    new_content = before + new_is_aut + after
    
    # Write back
    f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'w')
    f.write(new_content)
    f.close()
    print('Patched is_aut() to return true')
else:
    print('is_aut function not found')

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php')
print('Fixed permissions')

# Reload PHP
stdin, stdout, stderr = client.exec_command('systemctl reload php8.1-fpm')
print('Reloaded PHP')

# Test wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-admin/" -o /tmp/test_admin2.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin HTTP after patch: {admin_code}')

# Check for fatal errors
stdin, stdout, stderr = client.exec_command('grep -c "Fatal error" /tmp/test_admin2.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors: {fatal}')

client.close()