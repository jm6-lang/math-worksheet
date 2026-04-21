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

# The original require.php loads BEFORE codestar-framework (file #4 vs #5).
# So the original flow was:
# 1. inc/code/require.php → defines ZibFileAut + loads file.php etc.
# 2. inc/codestar-framework/codestar-framework.php → tries to load code/file.php
#    but require_once skips it because it was already loaded
#
# Now with our stub:
# 1. inc/code/require.php → our stub (no ZibFileAut)
# 2. inc/codestar-framework/codestar-framework.php → loads code/file.php → defines ZibFileAut
#    → OK, no conflict!
#
# But wait, the error says "Cannot declare class ZibFileAut, because the name is already in use"
# This means ZibFileAut IS being defined twice. 
# 
# Let me check: maybe our stub_v2 with class_exists() guard actually worked for some classes
# but NOT for ZibFileAut because file.php is loaded AFTER our stub?
#
# Actually no - with require_once, file.php would only be loaded once.
# The issue might be that file.php is loaded by BOTH codestar-framework AND something else.
#
# The simplest fix: just DON'T define ZibFileAut in the stub.

stub_v3 = """<?php
/**
 * Stub replacement for inc/code/require.php
 * Skips obfuscated code that makes blocking network requests
 * Only defines classes/functions not provided by other code/ files
 */

// ZibAut class - authorization (defined in code.php, but code.php is obfuscated and blocks)
// Since we can't load code.php, we define it here
if (!class_exists('ZibAut')) {
    class ZibAut {
        public static function is_local($url = '') { return false; }
        public static function aut_required() { return false; }
        public static function is_aut() { return true; }
        public static function replace_url($url) { return $url; }
        public static function delete() { return; }
    }
}

// ZibFileAut is defined in code/file.php which is loaded by codestar-framework
// Do NOT define it here

// ZibCodeAut is defined in code/aut.php and code/tool.php
// Do NOT define it here

// ZibCodeUpdeta is defined in code/update.php
// Do NOT define it here

// ZibToolRequire was defined in the ORIGINAL require.php itself
if (!class_exists('ZibToolRequire')) {
    class ZibToolRequire {
        public static function init() {}
    }
}

// Functions that may be needed
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
    f.write(stub_v3)
sftp.close()

print('Wrote stub v3 (no ZibFileAut, ZibCodeAut, ZibCodeUpdeta)')

# Test
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'Frontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

# Check for errors
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal\\|error" | grep -v "#error-page\\|wp-die\\|error-page\\|error code" | head -5')
if out:
    print(f'Errors: {out[:500]}')
else:
    print('No errors')

# Check page content
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -5')
print(f'Page start: {out[:300]}')

# Show page title
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "<title>[^<]*</title>" | head -1')
print(f'Title: {out}')

client.close()