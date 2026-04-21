import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

def run_cmd(cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

# Restore original inc.php first
run_cmd('cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')

# Now modify inc.php to skip only inc/code/require
# We need to keep the zib_require function and the HTTPS filter, but skip the
# code/require file from the array

fix_py = """import sys

path = '/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Replace the line 'inc/code/require', with a comment
content = content.replace(
    "    'inc/code/require',",
    "    // 'inc/code/require',  // DISABLED: causes blocking network calls",
    1  # only first occurrence
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched inc.php to skip code/require')
"""

sftp = client.open_sftp()
with sftp.file('/tmp/patch_inc.py', 'w') as f:
    f.write(fix_py)
sftp.close()

run_cmd('python3 /tmp/patch_inc.py')

# Verify
out = run_cmd("grep -n 'code/require\\|DISABLED' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php")
print(f'Verify: {out}')

# Restore original functions.php
run_cmd('cp /tmp/zibll_functions_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/functions.php')

# Restart and test
run_cmd('systemctl restart php8.1-fpm')
time.sleep(2)

print('\n=== Testing site with code/require disabled ===')
out = run_cmd('curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'Frontend: {out}')

out = run_cmd('curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

# Check content
out = run_cmd('curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -5')
print(f'\nContent: {out[:500]}')

# Check for errors
out = run_cmd('curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal\\|error\\|warning" | head -5')
if out:
    print(f'Errors: {out[:500]}')
else:
    print('No errors found in page')

client.close()