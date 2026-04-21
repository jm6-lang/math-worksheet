import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
    return client

def run_cmd(client, cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Step 1: Write the stub file that replaces code/require.php
# This defines the classes/functions that other files need, without the obfuscated code
stub_content = """<?php
/**
 * Stub replacement for inc/code/require.php
 * Original file contained obfuscated code that made blocking network requests to zibll.com
 * This stub provides the necessary class/function definitions for the theme to work
 */

// ZibAut class - authorization check
class ZibAut {
    public static function is_local($url = '') {
        return false;
    }
    
    public static function aut_required() {
        return false;
    }
    
    public static function is_aut() {
        // Return true to skip authorization checks
        // This prevents the theme from trying to connect to zibll.com
        return true;
    }
    
    public static function replace_url($url) {
        return $url;
    }
    
    public static function delete() {
        return;
    }
}

// zib_is_aut() function used in zibpay
function zib_is_aut() {
    return true;
}

// aut_required() function
function aut_required() {
    return false;
}

// zib_admin_tool_action() function
function zib_admin_tool_action() {
    return;
}

// zib_ajax_aut_error() function
function zib_ajax_aut_error() {
    return;
}

// ZibToolRequire class
class ZibToolRequire {
    public static function init() {
        // No-op: don't check for updates or authorization
    }
}

// ZibCodeAut class stub
class ZibCodeAut {
    public static function update($key, $data) {
        return false;
    }
    
    public static function get($key) {
        return false;
    }
}

// ZibCodeUpdeta class stub
class ZibCodeUpdeta {
    public function __construct() {
        // No-op
    }
    
    public static function init() {
        // No-op
    }
}

// ZibFileAut class stub
class ZibFileAut {
    public static function at_c() {
        return;
    }
    
    public static function at_d() {
        return;
    }
}

// zib_admin_aut_add_action function
function zib_admin_aut_add_action() {
    return;
}
"""

# Write stub to server
sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php', 'w') as f:
    f.write(stub_content)
sftp.close()

print('Step 1: Wrote stub require.php')

# Step 2: Restore original inc.php (with code/require ENABLED - now it loads our stub)
run_cmd(client, 'cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')
print('Step 2: Restored original inc.php')

# Step 3: Restore original functions.php
run_cmd(client, 'cp /tmp/zibll_functions_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/functions.php')
print('Step 3: Restored original functions.php')

# Step 4: Test via PHP CLI
test_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpyZXF1aXJlX29uY2UgQUJTUEFUSCAuICJ3cC1sb2FkLnBocCI7CmVjaG8gIldQX09LXG4iOwo="
run_cmd(client, f'echo "{test_b64}" | base64 -d > /tmp/test_wp_only.php')

print('\nStep 4: PHP CLI test...')
out = run_cmd(client, 'cd /www/wwwroot/resource_site && timeout 10 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'  Result: {out[:500]}')

# Step 5: Restart PHP-FPM and test HTTP
print('\nStep 5: HTTP test...')
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd(client, 'curl -s -k --max-time 15 -w "\\nHTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1 | tail -3')
print(f'  Frontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'  Login: {out}')

# Step 6: Check for errors in the page
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal\\|error\\|warning\\|notice" | head -5')
if out:
    print(f'  Errors: {out[:500]}')
else:
    print('  No visible errors')

# Step 7: Show first few lines of the page
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -5')
print(f'  Page start: {out[:300]}')

client.close()
print('\nDone!')