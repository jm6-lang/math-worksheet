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

# Restore original inc.php
run_cmd('cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')

# Strategy: use PHP pcntl alarm to detect which file hangs
# Create a test script that loads WP with Zibll theme but with timeouts per file
test_script = '''<?php
// /tmp/test_load.php
// Load WP without themes first
define('WP_USE_THEMES', false);
$_SERVER['HTTP_HOST'] = 'skillxm.cn';
$_SERVER['REQUEST_URI'] = '/';
$_SERVER['HTTPS'] = 'on';

define('ABSPATH', '/www/wwwroot/resource_site/');
$_SERVER['DOCUMENT_ROOT'] = '/www/wwwroot/resource_site';

// We need to manually bootstrap WP
require_once ABSPATH . 'wp-load.php';

echo "WP loaded OK\\n";
flush();

// Now try loading the Zibll theme functions file
$theme_file = '/www/wwwroot/resource_site/wp-content/themes/zibll/functions.php';

// Use a child process to test with timeout
$descriptors = array(
    0 => array('pipe', 'r'),
    1 => array('pipe', 'w'),
    2 => array('pipe', 'w'),
);

// Test: what happens if we just include functions.php with a 5s timeout?
$cmd = "cd /www/wwwroot/resource_site && timeout 5 php -d display_errors=1 "
     . "-d auto_prepend_file= "
     . "-r '"
     . "define(\"ABSPATH\", \"/www/wwwroot/resource_site/\");"
     . "$_SERVER[\"HTTP_HOST\"]=\"skillxm.cn\";"
     . "$_SERVER[\"REQUEST_URI\"]=\"/\";"
     . "$_SERVER[\"HTTPS\"]=\"on\";"
     . "$_SERVER[\"DOCUMENT_ROOT\"]=\"/www/wwwroot/resource_site\";"
     . "require_once ABSPATH . \"wp-load.php\";"
     . "echo \"WP_OK\\n\";"
     . "require \"/www/wwwroot/resource_site/wp-content/themes/zibll/functions.php\";"
     . "echo \"THEME_OK\\n\";"
     . "' 2>&1";

echo "Running test...\\n";
flush();
passthru($cmd, $exitcode);
echo "Exit code: $exitcode\\n";
'''

sftp = client.open_sftp()
with sftp.file('/tmp/test_load.php', 'w') as f:
    f.write(test_script)
sftp.close()

print('=== Test: Load WP + Zibll functions.php with 5s timeout ===')
out = run_cmd('timeout 15 php /tmp/test_load.php 2>&1', timeout=20)
print(out[:3000])

# Also: let's just check what the actual white page returns
# Maybe it's an nginx issue, not PHP?
print('\n=== Nginx error log ===')
out = run_cmd('tail -10 /www/wwwlogs/skillxm.cn.error.log 2>&1')
print(out[:1000])

print('\n=== Check if PHP-FPM is running ===')
out = run_cmd('systemctl is-active php8.1-fpm 2>&1')
print(out)

# Check if the page returns any headers
print('\n=== Response headers ===')
out = run_cmd('curl -s -k -D - --max-time 5 -o /dev/null https://127.0.0.1/ 2>&1')
print(out[:500])

client.close()