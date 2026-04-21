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

# Strategy: Replace require.php with a stub that:
# 1. Provides ZibAut, ZibToolRequire, and other needed stubs
# 2. But ALSO loads code.php (which provides the eval'd code for admin-options etc)
# 3. Does NOT load aut.php, update.php, new_aut.php (which likely connect to zibll.com)

stub_v5 = """<?php
/**
 * Stub replacement for inc/code/require.php
 * Loads code.php for eval'd code support, but skips blocking network calls
 */

// Load code.php which contains eval'd functions used by admin-options.php etc.
// This file defines the obfuscated functions that preprocess theme options
require_once dirname(__FILE__) . '/code.php';

// Provide stub classes that were originally defined in other code/ files
// (aut.php, tool.php, update.php, file.php etc.)

if (!class_exists('ZibAut')) {
    class ZibAut {
        public static function is_local($url = '') { return false; }
        public static function aut_required() { return false; }
        public static function is_aut() { return true; }
        public static function is_update() { return 'null'; }
        public static function replace_url($url) { return $url; }
        public static function delete() { return; }
    }
}

if (!class_exists('ZibToolRequire')) {
    class ZibToolRequire {
        public static function init() {}
    }
}

if (!class_exists('ZibCodeAut')) {
    class ZibCodeAut {
        public static function update($key, $data) { return false; }
        public static function get($key) { return false; }
    }
}

if (!class_exists('ZibCodeUpdeta')) {
    class ZibCodeUpdeta {
        public function __construct() {}
        public static function init() {}
    }
}

if (!class_exists('ZibFileAut')) {
    class ZibFileAut {
        public static function at_c() {}
        public static function at_d() {}
    }
}

if (!function_exists('zib_is_aut')) {
    function zib_is_aut() { return true; }
}
if (!function_exists('zib_admin_tool_action')) {
    function zib_admin_tool_action() { return; }
}
if (!function_exists('zib_ajax_aut_error')) {
    function zib_ajax_aut_error() { return; }
}
if (!function_exists('zib_admin_aut_add_action')) {
    function zib_admin_aut_add_action() { return; }
}
"""

sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php', 'w') as f:
    f.write(stub_v5)
sftp.close()

print('Wrote stub v5 (loads code.php + provides stubs)')

# Test via PHP CLI first
test_b64 = "PD9waHAKJF9TRVJWRVJbIkhUVFBfSE9TVCJdID0gInNraWxseG0uY24iOwokX1NFUlZFUlsiUkVRVUVTVF9VUkkiXSA9ICIvIjsKJF9TRVJWRVJbIkhUVFBTIl0gPSAib24iOwokX1NFUlZFUlsiRE9DVU1FTlRfUk9PVCJdID0gIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlIjsKJF9TRVJWRVJbIlNFUlZFUl9QT1JUIl0gPSAiNDQzIjsKZGVmaW5lKCJBQlNQQVRIIiwgIi93d3cvd3d3cm9vdC9yZXNvdXJjZV9zaXRlLyIpOwpyZXF1aXJlX29uY2UgQUJTUEFUSCAuICJ3cC1sb2FkLnBocCI7CmVjaG8gIldQX09LXG4iOwo="
run_cmd(client, f'echo "{test_b64}" | base64 -d > /tmp/test_wp_only.php')

print('PHP CLI test...')
out = run_cmd(client, 'cd /www/wwwroot/resource_site && timeout 10 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'  Result: {out[:500]}')

# HTTP test
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'\nFrontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "<title>[^<]*</title>" | head -1')
print(f'Title: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal\\|parse error" | head -3')
if out:
    print(f'Errors: {out[:500]}')
else:
    print('No errors!')

client.close()