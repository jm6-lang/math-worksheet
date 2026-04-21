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

# Check inc/code/require.php content
print('=== inc/code/require.php ===')
out = run_cmd("wc -c /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php 2>&1")
print(f'Size: {out} bytes')

out = run_cmd("head -5 /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php 2>&1")
print(out[:500])

# Now the real test: use a PHP script to load WP, then load each theme file one by one
# and time each one
test_script = r'''
<?php
// Save as /tmp/test_zibll.php
define('ABSPATH', '/www/wwwroot/resource_site/');
define('WPINC', 'wp-includes');

// Minimal WP bootstrap
require_once ABSPATH . 'wp-load.php';

// Now test loading each file
$files = array(
    'inc/dependent.php',
    'vendor/autoload.php',
    'inc/class/class.php',
    'inc/code/require.php',
    'inc/codestar-framework/codestar-framework.php',
);

$theme_dir = '/www/wwwroot/resource_site/wp-content/themes/zibll/';

foreach ($files as $f) {
    $path = $theme_dir . $f;
    $start = microtime(true);
    
    // Set a 3-second alarm
    set_error_handler(function() {});
    
    // Try to load the file
    ob_start();
    try {
        require_once $path;
        $ok = true;
    } catch (Exception $e) {
        $ok = false;
    }
    ob_end_clean();
    
    $elapsed = round((microtime(true) - $start) * 1000);
    echo "$f: " . ($ok ? "OK" : "FAIL") . " (${elapsed}ms)\n";
    flush();
}
'''

stdin, stdout, stderr = client.exec_command(f'cat > /tmp/test_zibll.php << \'PHPEOF\'\n{test_script}\nPHPEOF')
time.sleep(1)

print('\n=== Testing file load times ===')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 15 php /tmp/test_zibll.php 2>&1', timeout=20)
print(out[:2000])

client.close()