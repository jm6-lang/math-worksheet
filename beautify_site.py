import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[BEAUTIFY] Update site settings for jichuanglm.cn style')

# Set site name, description, and URL
sql = """USE wp_skillxm;
UPDATE wp_options SET option_value = '极创项目网' WHERE option_name = 'blogname';
UPDATE wp_options SET option_value = '网创项目资源站-副业项目-创业项目-搞钱项目' WHERE option_name = 'blogdescription';
UPDATE wp_options SET option_value = 'https://skillxm.cn' WHERE option_name = 'siteurl';
UPDATE wp_options SET option_value = 'https://skillxm.cn' WHERE option_name = 'home';
"""

sftp = client.open_sftp()
f = sftp.file('/tmp/site_beautify.sql', 'w')
f.write(sql)
f.close()

stdin, stdout, stderr = client.exec_command('mysql -u root < /tmp/site_beautify.sql 2>&1')
print('Site info updated')

# Now set Zibll theme options via PHP to handle serialization properly
# We'll use WordPress CLI-like approach through a PHP script

php_script = """<?php
define('WP_USE_THEMES', false);
require_once('/www/wwwroot/resource_site/wp-load.php');

// Get current options
$opts = get_option('zibll_options', array());

// Set footer copyright (key name from Zibll theme)
$opts['footer_copyright'] = 'Copyright &copy; 2026 &middot; <a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow noopener" class="muted">鲁ICP备2025156080号-1</a> &middot; 由<a href="https://www.jichuanglm.cn/" target="_blank">极创联盟</a>强力驱动';

// Set site run time
$opts['footer_run_time'] = 1;

// Navigation menu color
$opts['navbar_style'] = '1';

// Theme color scheme
$opts['theme_skin'] = '';

// Sidebar position
$opts['sidebar_position'] = 'right';

update_option('zibll_options', $opts);

echo "Zibll options updated\\n";

// Also set nav menus
$locations = get_nav_menu_locations();
echo "Current menus: " . json_encode($locations) . "\\n";

// Create a nav menu if none exists
$menu_name = 'Main Navigation';
$menu_exists = wp_get_nav_menu_object($menu_name);
if (!$menu_exists) {
    $menu_id = wp_create_nav_menu($menu_name);
    echo "Created menu: $menu_id\\n";
    
    // Add some menu items
    wp_update_nav_menu_item($menu_id, 0, array(
        'menu-item-title' => '首页',
        'menu-item-url' => home_url('/'),
        'menu-item-status' => 'publish',
    ));
    wp_update_nav_menu_item($menu_id, 0, array(
        'menu-item-title' => '项目列表',
        'menu-item-url' => home_url('/category/default/'),
        'menu-item-status' => 'publish',
    ));
    wp_update_nav_menu_item($menu_id, 0, array(
        'menu-item-title' => '会员中心',
        'menu-item-url' => home_url('/user/'),
        'menu-item-status' => 'publish',
    ));
    
    // Set menu location
    set_theme_mod('nav_menu_locations', array('primary' => $menu_id));
    echo "Menu items added\\n";
}

echo "DONE\\n";
"""

f = sftp.file('/tmp/setup_theme.php', 'w')
f.write(php_script)
f.close()

# Execute PHP script
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && php /tmp/setup_theme.php 2>&1')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print('PHP result:', result)

errors = stderr.read().decode('utf-8', errors='ignore').strip()
if errors:
    print('PHP errors:', errors[:500])

# Verify site
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ | grep -oP "<title>.*?</title>"')
title = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage title: {title}')

client.close()
print('[DONE]')