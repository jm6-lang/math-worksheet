import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Rewrite wp-config.php properly')

# Get the original wp-config values from database
# We know: DB_NAME=wp_skillxm, DB_USER=wp_user, DB_PASS=gMshA29CshK5, DB_HOST=localhost

# Write a clean wp-config.php
wp_config = """<?php
/**
 * WordPress Configuration
 */

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

define('DB_NAME', 'wp_skillxm');
define('DB_USER', 'wp_user');
define('DB_PASSWORD', 'gMshA29CshK5');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATE', '');

$table_prefix = 'wp_';

define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', true);

/* That's all, stop editing! */
if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}

require_once ABSPATH . 'wp-settings.php';
"""

# Write using heredoc to avoid escaping issues
cmd = f"cat > /www/wwwroot/resource_site/wp-config.php << 'WPEOF'\n{wp_config}\nWPEOF"
stdin, stdout, stderr = client.exec_command(cmd)
print('Write result:', stderr.read().decode('utf-8', errors='ignore').strip())

# Verify
stdin, stdout, stderr = client.exec_command('head -3 /www/wwwroot/resource_site/wp-config.php')
print('Top:', stdout.read().decode('utf-8', errors='ignore').strip())

# Syntax check
stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-config.php 2>&1')
print('Syntax:', stdout.read().decode('utf-8', errors='ignore').strip())

# Fix permissions
stdin, stdout, stderr = client.exec_command('chown www-data:www-data /www/wwwroot/resource_site/wp-config.php && chmod 640 /www/wwwroot/resource_site/wp-config.php')

# Restart PHP
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm')
time.sleep(2)

# Test
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | head -5')
page = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage: {page[:500]}')

stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | wc -c')
size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage size: {size} bytes')

client.close()