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

# Test 1: Load just wp-load.php WITHOUT theme (with twentytwentyfour)
print('=== Test 1: wp-load.php only (Zibll is DB theme) ===')
php1_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpyZXF1aXJlX29uY2UgQUJTUEFUSCAuICJ3cC1sb2FkLnBocCI7CmVjaG8gIldQX09LXG4iOwo="
run_cmd(f'echo "{php1_b64}" | base64 -d > /tmp/test_wp_only.php')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Result: {out[:500]}')

# Test 2: Load wp-load.php WITHOUT loading theme
# To do this, switch DB theme to twentytwentyfour first, then test
print('\n=== Test 2: Switch to twentytwentyfour, test wp-load.php ===')
run_cmd("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'twentytwentyfour' WHERE option_name IN ('template', 'stylesheet');\"")
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Result: {out[:500]}')

# Now we know wp-load.php works without Zibll. Let's switch back to Zibll
# and try to isolate what blocks.
# The issue is that wp-load.php eventually loads the active theme's functions.php
# Let's test if wp-settings.php (loaded by wp-load) is what triggers theme loading

# Test 3: with Zibll active, test which part of WP init hangs
print('\n=== Test 3: Switch to Zibll, test step by step ===')
run_cmd("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'zibll' WHERE option_name IN ('template', 'stylesheet');\"")

# Check if wp-config.php has any external calls
print('\n=== wp-config.php (check for external URLs) ===')
out = run_cmd("grep -i 'curl\\|fopen\\|file_get_contents\\|stream_context\\|wp_remote\\|include\\|require' /www/wwwroot/resource_site/wp-config.php 2>&1")
print(out[:500])

# Check if any mu-plugin loads
print('\n=== mu-plugins ===')
out = run_cmd('ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>&1')
print(out[:500])

# Check if any active plugin might be blocking
print('\n=== Active plugins ===')
out = run_cmd("mysql -u root -N -e \"SELECT option_value FROM wp_skillxm.wp_options WHERE option_name='active_plugins';\" 2>&1")
print(out[:2000])

client.close()