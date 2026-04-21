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

# require.php originally loads other code/ files. Let me check what it requires:
# I need to see the actual require statements in the original require.php
# But it's obfuscated... However, I know the files in the code/ directory:
# action.php, aut.php, code.php, file.php, new_aut.php, require.php, tool.php, update.php
#
# The original require.php likely includes some of these via eval'd code.
# Since file.php defines ZibFileAut, it's probably included by require.php.
#
# I need to NOT define ZibFileAut in the stub, OR figure out which files
# are loaded by require.php and handle conflicts.
#
# Actually, the simplest approach: the original require.php IS the entry point
# that loads ALL the other code/*.php files. So if I replace it with a stub,
# I shouldn't define classes that are already defined elsewhere.
#
# But wait - the error says ZibFileAut is in file.php:151, which means file.php
# IS being loaded by something else (not require.php, since we replaced that).
#
# Let me check: what loads file.php?

print('=== What loads file.php? ===')
out = run_cmd(client, "grep -rn 'file.php\\|file\\.php' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>&1 | grep -v 'code/\\|Binary' | head -20")
print(out[:1000])

# Actually, the original require.php at line 126 calls ZibToolRequire::init()
# which is defined in the same file. But the original file also likely loads
# other code/ files via require/include.
# 
# Let me check: what does the ORIGINAL require.php look like around the class definition
# The class is at line 126. Let me see the surrounding context.

print('\n=== Original require.php backup check ===')
# Check if we have the original backed up
out = run_cmd(client, 'ls -la /tmp/themes_backup/inc/code/require.php 2>&1')
print(out)

# We have the backup. Let me check if require.php includes other files
# by searching for 'require' patterns in the file
out = run_cmd(client, "strings /tmp/themes_backup/inc/code/require.php 2>&1 | grep -i 'require\\|include\\|file\\.php\\|action\\.php\\|aut\\.php\\|code\\.php\\|tool\\.php\\|update\\.php' | head -20")
print(f'\nStrings in original require.php: {out[:500]}')

# The obfuscated code makes it hard to tell. Let me try another approach:
# Just make the stub NOT define ZibFileAut and see what other errors we get
stub_v2 = """<?php
/**
 * Stub replacement for inc/code/require.php
 * Provides necessary class/function definitions without obfuscated blocking code
 */

// ZibAut class - authorization check
if (!class_exists('ZibAut')) {
    class ZibAut {
        public static function is_local($url = '') {
            return false;
        }
        public static function aut_required() {
            return false;
        }
        public static function is_aut() {
            return true;
        }
        public static function replace_url($url) {
            return $url;
        }
        public static function delete() {
            return;
        }
    }
}

if (!function_exists('zib_is_aut')) {
    function zib_is_aut() {
        return true;
    }
}

if (!function_exists('aut_required')) {
    function aut_required() {
        return false;
    }
}

if (!function_exists('zib_admin_tool_action')) {
    function zib_admin_tool_action() {
        return;
    }
}

if (!function_exists('zib_ajax_aut_error')) {
    function zib_ajax_aut_error() {
        return;
    }
}

if (!class_exists('ZibToolRequire')) {
    class ZibToolRequire {
        public static function init() {
            // No-op
        }
    }
}

if (!class_exists('ZibCodeAut')) {
    class ZibCodeAut {
        public static function update($key, $data) {
            return false;
        }
        public static function get($key) {
            return false;
        }
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

if (!function_exists('zib_admin_aut_add_action')) {
    function zib_admin_aut_add_action() {}
}
"""

sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php', 'w') as f:
    f.write(stub_v2)
sftp.close()

print('Wrote stub v2 with class_exists guards')

# Test
run_cmd(client, 'systemctl restart php8.1-fpm')
time.sleep(2)

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'\nFrontend: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | grep -i "fatal\\|error\\|warning" | grep -v "wp-" | head -5')
if out:
    print(f'Errors: {out[:500]}')
else:
    print('No errors')

out = run_cmd(client, 'curl -s -k --max-time 15 https://127.0.0.1/ 2>&1 | head -5')
print(f'Page: {out[:300]}')

client.close()