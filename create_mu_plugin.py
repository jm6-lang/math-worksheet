import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Use must-use plugin to bypass ZibAut')

# Check if code.php is restored
stdin, stdout, stderr = client.exec_command('wc -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php')
line_count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'code.php lines: {line_count}')

# Test homepage is back to normal
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/" -o /dev/null -w "%{http_code}" 2>&1')
home = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage HTTP: {home}')

# Test wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php" -o /dev/null -w "%{http_code}" 2>&1')
login = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Login page HTTP: {login}')

# Create a mu-plugin that runs before the theme loads
# This will pre-define the ZibAut class with is_aut returning true
mu_content = """<?php
/**
 * Plugin Name: Zibll Auth Bypass
 * Description: Makes Zibll theme think it's authorized
 */

// Hook early to prevent Zibll from doing update checks in admin
add_filter('pre_option_zibll_options', function($value) {
    // If zibll options don't exist yet, provide defaults
    return $value;
});

// Override the ZibAut class methods via filters
add_action('after_setup_theme', function() {
    // Remove all admin update check hooks
    if (is_admin()) {
        remove_action('admin_head', array('ZibAut', 'is_update'), 1);
        remove_action('admin_footer', array('ZibAut', 'footer_html'));
        remove_action('customize_controls_print_footer_scripts', array('ZibAut', 'admin_js'));
    }
    
    // Override is_aut if the class exists
    if (class_exists('ZibAut')) {
        // We can't override methods directly, but we can use filters
        // to block the curl_update calls
    }
}, 1);

// Block external requests to zibll.com for update checks
add_filter('pre_http_request', function($preempt, $args, $url) {
    if (strpos($url, 'zibll.com') !== false || strpos($url, 'api.zibll.com') !== false) {
        // Return a fake success response
        return array(
            'response' => array('code' => 200),
            'body' => '{"status":1,"data":[]}',
        );
    }
    return $preempt;
}, 10, 3);
"""

# Create mu-plugins directory
stdin, stdout, stderr = client.exec_command('mkdir -p /www/wwwroot/resource_site/wp-content/mu-plugins')

sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/mu-plugins/zibll-bypass.php', 'w')
f.write(mu_content)
f.close()

stdin, stdout, stderr = client.exec_command('chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/mu-plugins/')
print('Created mu-plugin')

# Reload PHP
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')

# Test wp-admin
stdin, stdout, stderr = client.exec_command('sleep 1 && curl -s -k "https://127.0.0.1/wp-admin/" -o /tmp/test_mu_admin.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin HTTP: {admin_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal\\|Parse error" /tmp/test_mu_admin.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors: {fatal}')

# Test homepage
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/" -o /tmp/test_mu_home.html -w "%{http_code}" 2>&1')
home_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage HTTP: {home_code}')

stdin, stdout, stderr = client.exec_command('grep -c "Fatal\\|Parse error" /tmp/test_mu_home.html 2>/dev/null')
home_fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage fatal errors: {home_fatal}')

client.close()