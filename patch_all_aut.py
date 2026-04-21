import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Patch all ZibAut methods')

# Read current code.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

# Find all function definitions in the ZibAut class
import re
# Find positions of all functions
func_pattern = re.compile(r'function\s+(\w+)\s*\(', re.DOTALL)
matches = list(func_pattern.finditer(content))

print(f'Found {len(matches)} functions')

# Patch curl_update and is_update
# First find curl_update
for m in matches:
    name = m.group(1)
    if name in ('curl_update', 'is_update', 'is_aut'):
        pos = m.start()
        print(f'Patching {name} at position {pos}')
        
        # Find the end of this function (next function or end of class)
        next_pos = len(content)
        for nm in matches:
            if nm.start() > pos and nm.start() < next_pos:
                next_pos = nm.start()
        
        # Replace function
        before = content[:pos]
        after = content[next_pos:]
        new_func = f'function {name}($a=null,$b=null){{return $a==="null"?null:$a;}}\n    '
        content = before + new_func + after

# Write back
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'w')
f.write(content)
f.close()

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php')
stdin, stdout, stderr = client.exec_command('systemctl reload php8.1-fpm')

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-admin/" -o /tmp/test_admin3.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin HTTP: {admin_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal" /tmp/test_admin3.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors: {fatal}')

# Also test homepage
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/" -o /tmp/test_home3.html -w "%{http_code}" 2>&1')
home_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage HTTP: {home_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal\\|Error" /tmp/test_home3.html 2>/dev/null')
home_errs = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage errors: {home_errs}')

client.close()