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

# Make sure Zibll is the active theme
run_cmd("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'zibll' WHERE option_name IN ('template', 'stylesheet');\"")

# Step 1: Backup functions.php
run_cmd('cp /www/wwwroot/resource_site/wp-content/themes/zibll/functions.php /tmp/zibll_functions_backup.php')

# Step 2: Comment out the require_once inc.php line
fix_py = r"""import sys

path = '/www/wwwroot/resource_site/wp-content/themes/zibll/functions.php'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Comment out the require_once inc.php line
content = content.replace(
    "require_once get_theme_file_path('/inc/inc.php');",
    "// require_once get_theme_file_path('/inc/inc.php');"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Commented out inc.php require')
"""

sftp = client.open_sftp()
with sftp.file('/tmp/fix_functions.py', 'w') as f:
    f.write(fix_py)
sftp.close()

run_cmd('python3 /tmp/fix_functions.py')
print('Modified functions.php')

# Step 3: Test with no inc.php loaded - does site at least load?
run_cmd('systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd('curl -s -k --max-time 10 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'\nWithout inc.php - Frontend: {out}')

out = run_cmd('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -3')
print(f'Content: {out[:300]}')

# Step 4: Now test via PHP CLI too
php_test_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpyZXF1aXJlX29uY2UgQUJTUEFUSCAuICJ3cC1sb2FkLnBocCI7CmVjaG8gIldQX09LXG4iOwo="
run_cmd(f'echo "{php_test_b64}" | base64 -d > /tmp/test_wp_only.php')

print('\n=== PHP CLI test (no inc.php) ===')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Result: {out[:500]}')

client.close()