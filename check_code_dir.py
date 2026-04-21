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

# Test via PHP CLI - this should show actual errors
php_test_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpyZXF1aXJlX29uY2UgQUJTUEFUSCAuICJ3cC1sb2FkLnBocCI7CmVjaG8gIldQX09LXG4iOwo="
run_cmd(f'echo "{php_test_b64}" | base64 -d > /tmp/test_wp_only.php')

print('=== PHP CLI test with code/require disabled ===')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 15 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=20)
print(f'Result: {out[:3000]}')

# Also check what functions/classes code/require.php defines
# by looking at what it requires/includes
print('\n=== Files that code/require.php includes ===')
out = run_cmd("ls /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/ 2>&1")
print(out[:500])

# Check what's in the code directory
out = run_cmd("ls -la /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/ 2>&1")
print(out[:500])

# Check what new_aut.php references (it was modified before)
print('\n=== new_aut.php ===')
out = run_cmd("head -20 /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php 2>&1")
print(out[:500])

client.close()