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

# Empty inc.php works! So the problem is in the inc.php file loading process.
# Now let's progressively add content to find what blocks.
# 
# The key suspects are:
# 1. get_template_directory_uri() - could trigger HTTP request
# 2. wp_get_theme() - could do something slow
# 3. The actual file loading (code/require.php etc)

# Test: inc.php with just the function definitions and HTTPS filter, NO file loading
test_inc = r"""<?php
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
echo 'INC_INIT_OK';
"""

sftp = client.open_sftp()
with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php', 'w') as f:
    f.write(test_inc)
sftp.close()

print('=== Test: inc.php with defines only, no file loading ===')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Result: {out[:500]}')

# Now add file loading one at a time
files_to_test = [
    'inc/dependent',
    'vendor/autoload',
    'inc/class/class',
    'inc/code/require',
    'inc/codestar-framework/codestar-framework',
    'inc/widgets/widget-class',
    'inc/options/options',
    'inc/functions/functions',
    'inc/widgets/widget-index',
    'oauth/oauth',
    'zibpay/functions',
    'action/function',
    'inc/functions/rest-api/function',
    'inc/csf-framework/classes/zib-csf.class',
]

for i, f in enumerate(files_to_test):
    test_inc_with_files = test_inc + f"\nzib_require('{f}', true);\necho 'FILE_{i+1}_OK';\n"
    
    with sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php', 'w') as fh:
        fh.write(test_inc_with_files)
    sftp.close()
    
    # Re-open sftp if needed
    sftp = client.open_sftp()
    
    out = run_cmd(f'cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
    
    if 'WP_OK' in out and f'FILE_{i+1}_OK' in out:
        print(f'  File {i+1} ({f}): OK')
    elif 'WP_OK' in out:
        print(f'  File {i+1} ({f}): WP loaded but file error - {out[:200]}')
    elif not out:
        print(f'  File {i+1} ({f}): HANG (timeout)')
    else:
        print(f'  File {i+1} ({f}): ERROR - {out[:200]}')

# Restore
run_cmd('cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')
print('\nRestored original inc.php')
client.close()