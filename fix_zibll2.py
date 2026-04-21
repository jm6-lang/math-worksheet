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

# Restore inc.php from backup first
run_cmd('cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')
print('Restored inc.php from backup')

# Now use python on the server to do the replacement properly
py_fix = r'''
import sys

path = '/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

new_lines = []
changed = False
for line in lines:
    if "'inc/code/require'" in line and not line.strip().startswith('//'):
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + "// " + line.lstrip())
        changed = True
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'Changed: {changed}')
'''

sftp = client.open_sftp()
with sftp.file('/tmp/fix_inc.py', 'w') as f:
    f.write(py_fix)
sftp.close()

out = run_cmd('python3 /tmp/fix_inc.py 2>&1')
print(out)

# Verify
out = run_cmd("grep -n 'code/require' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php")
print(f'Verify: {out}')

# Restart PHP-FPM and test
run_cmd('systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd('curl -s -k --max-time 10 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'\nFrontend: {out}')

out = run_cmd('curl -s -k --max-time 10 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

# Check actual content
out = run_cmd('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -3')
print(f'\nPage start: {out[:300]}')

client.close()