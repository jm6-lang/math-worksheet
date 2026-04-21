import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Run a PHP snippet to check get_stylesheet_directory_uri() and what styles are enqueued
stdin, stdout, stderr = client.exec_command(
    '''php -r "
    define('ABSPATH', '/www/wwwroot/skillxm.cn/public/');
    define('WPINC', 'wp-includes');
    define('WP_CONTENT_DIR', '/www/wwwroot/skillxm.cn/public/wp-content');
    
    // Load just enough to get template functions
    require_once '/www/wwwroot/skillxm.cn/public/wp-includes/theme.php';
    require_once '/www/wwwroot/skillxm.cn/public/wp-includes/functions.php';
    require_once '/www/wwwroot/skillxm.cn/public/wp-includes/wp-db.php';
    
    // Get template directory
    echo 'Template: ' . get_template_directory() . PHP_EOL;
    echo 'Stylesheet: ' . get_stylesheet_directory() . PHP_EOL;
    echo 'Template URI: ' . get_template_directory_uri() . PHP_EOL;
    echo 'Stylesheet URI: ' . get_stylesheet_directory_uri() . PHP_EOL;
    " 2>&1''',
    timeout=15
)
print('PHP path check:')
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

# Alternative: directly cat the custom.css file to see if it has our content
stdin, stdout, stderr = client.exec_command(
    'head -3 /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/custom.css 2>/dev/null || echo "no file"',
    timeout=10
)
print('\nskillxm custom.css:')
print(stdout.read().decode('utf-8', errors='replace'))

# Also check if there's a resource_site symlink to skillxm theme
stdin, stdout, stderr = client.exec_command(
    'ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/ 2>/dev/null | head -10',
    timeout=10
)
print('\nskillxm themes:')
print(stdout.read().decode('utf-8', errors='replace'))

client.close()
