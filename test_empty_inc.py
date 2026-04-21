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

# The issue might be that after code/require.php loads (or even during its load),
# something in the theme does a blocking HTTP request.
# 
# Wait - let me reconsider. Files 1-3 worked with the CUSTOM inc.php.
# But files 5-14 ALL hang even with the ORIGINAL inc.php (just code/require commented).
#
# The difference: the original inc.php has additional code BEFORE the zib_require() call:
# - HTTPS filter (add_filter)
# - define('ZIB_TEMPLATE_DIRECTORY_URI', get_template_directory_uri())
# - define('ZIB_ROOT_PATH', ...)  
# - define('ZIB_TEMP_DIR', ...)
# - $theme_data = wp_get_theme()
# - PHP version check
# - zib_require() function definition
#
# Could get_template_directory_uri() or wp_get_theme() make external HTTP calls?
# Unlikely for CLI. But the add_filter is fine too.
#
# Wait... maybe the problem is different. When I tested files 1-3 with custom inc.php,
# those files loaded fine. But maybe one of those files (like inc/dependent.php)
# does something async or sets up a shutdown handler that causes issues?
#
# Let me test with an EMPTY inc.php (no code at all, just <?php)

print('=== Test with completely empty inc.php ===')
sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php', 'w') as f:
    f.write('<?php\n// Empty inc.php\n')
sftp.close()

out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Empty inc.php: {out[:500]}')

# Test with just the defines and function
print('\n=== Test with defines + zib_require function only ===')
test_inc = """<?php
// Minimal inc.php
function zib_content_url_filter($url) {
    if (!preg_match('/^https/', $url)) {
        $home_url = home_url();
        if (preg_match('/^https', $home_url)) {
            $url = str_replace('http', 'https', $url);
        }
    }
    return $url;
}
add_filter('content_url', 'zib_content_url_filter');
define('ZIB_TEMPLATE_DIRECTORY_URI', get_template_directory_uri());
define('ZIB_ROOT_PATH', dirname(__DIR__) . '/');
define('ZIB_TEMP_DIR', apply_filters('zib_temp_dir', WP_CONTENT_DIR . '/zib-temp'));
$theme_data = wp_get_theme();
define('THEME_VERSION', $theme_data['Version']);

function zib_require($data, $is_once = false, $prefix = '') {
    if (is_array($data)) {
        foreach ($data as $d) {
            zib_require($d, $is_once, $prefix);
        }
    } else {
        if ($is_once) {
            require_once get_theme_file_path($prefix . $data . '.php');
        } else {
            require get_theme_file_path($prefix . $data . '.php');
        }
    }
}

// Now load files 1-3 only
echo 'Loading file 1...'; flush();
zib_require('inc/dependent', true);
echo 'OK\\n'; flush();

echo 'Loading file 2...'; flush();
zib_require('vendor/autoload', true);
echo 'OK\\n'; flush();

echo 'Loading file 3...'; flush();
zib_require('inc/class/class', true);
echo 'OK\\n'; flush();

echo 'Loading file 5 (codestar)...'; flush();
zib_require('inc/codestar-framework/codestar-framework', true);
echo 'OK\\n'; flush();

echo 'DONE\\n'; flush();
"""
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php', 'w') as f:
    f.write(test_inc)
sftp.close()

out = run_cmd('cd /www/wwwroot/resource_site && timeout 12 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=18)
print(f'Result: {out[:1000]}')

client.close()