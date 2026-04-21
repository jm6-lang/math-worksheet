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

# First, find what classes/functions code/require.php defines
# Search for class and function definitions in all code/ files
print('=== Classes/functions defined in code/ directory ===')

for fname in ['action.php', 'aut.php', 'code.php', 'file.php', 'new_aut.php', 'require.php', 'tool.php', 'update.php']:
    out = run_cmd(f'grep -n "function \\|class " /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/{fname} 2>&1 | grep -v "//\\|\\*" | head -10')
    if out:
        print(f'\n--- {fname} ---')
        print(out[:500])

# Now search for references to ZibAut and other code/ functions in other theme files
print('\n\n=== References to ZibAut ===')
out = run_cmd("grep -rn 'ZibAut\\|zib_aut\\|zib_admin_tool' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>&1 | grep -v 'inc/code/' | head -20")
print(out[:1000])

# Create a proper inc.php: original inc.php with code/require replaced by stubs
# Read the original inc.php
sftp = client.open_sftp()
with sftp.file('/tmp/inc_php_backup.php', 'r') as f:
    orig_inc = f.read().decode('utf-8', errors='replace')
sftp.close()

# Find the line number of 'inc/code/require' and comment it out
lines = orig_inc.split('\n')
new_lines = []
for line in lines:
    if "'inc/code/require'" in line and not line.strip().startswith('//'):
        indent = len(line) - len(line.lstrip())
        new_lines.append(' ' * indent + "// " + line.lstrip() + "  // DISABLED: blocking")
    else:
        new_lines.append(line)

new_inc = '\n'.join(new_lines)

# Write modified inc.php
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php', 'w') as f:
    f.write(new_inc)
sftp.close()

# Now test with PHP CLI - what errors do we get?
# The site should partially work but with some missing functions
print('\n=== Test: skip code/require, check what breaks ===')

# First create a test PHP that loads WP + theme and outputs errors
test_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpzZXRfZXJyb3JfaGFuZGxlcihmdW5jdGlvbigkZXJybm8sICRlcnJzdHIpIHsKICAgIGVjaG8gIkVSUk9SOiAkZXJyc3RyXG4iOwogICAgcmV0dXJuIGZhbHNlOwp9KTsKcmVxdWlyZV9vbmNlIEFCU1BBVEggLiAid3AtbG9hZC5waHAiOwplY2hvICJXUF9PS1xuIjsK"
run_cmd(f'echo "{test_b64}" | base64 -d > /tmp/test_wp_only.php')

# Use a short timeout since we know it might hang
out = run_cmd('cd /www/wwwroot/resource_site && timeout 6 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=10)
print(f'PHP CLI: {out[:2000]}')

# Also test via HTTP
run_cmd('systemctl restart php8.1-fpm')
time.sleep(2)
out = run_cmd('curl -s -k --max-time 10 -w "\\nHTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1 | tail -5')
print(f'\nHTTP: {out[:500]}')

client.close()