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

stub_v4 = """<?php
/**
 * Stub replacement for inc/code/require.php
 * Skips obfuscated code that makes blocking network requests to zibll.com
 */

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
    f.write(stub_v4)
sftp.close()

print('Wrote stub v4 with is_update()')

run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'Frontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -o "<title>[^<]*</title>" | head -1')
print(f'Title: {out}')

# Check for fatal errors
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal error" | head -3')
if out:
    print(f'Fatal: {out[:500]}')
else:
    print('No fatal errors!')

# Show first line
out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -1')
print(f'First line: {out[:200]}')

client.close()