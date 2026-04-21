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

def run_cmd(client, cmd, timeout=15):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        err = stderr.read().decode('utf-8', errors='replace').strip()
        return out, err
    except:
        return '[TIMEOUT]', ''

client = connect()

# 1. List all available themes
print('=== Available themes ===')
out, _ = run_cmd(client, 'ls -1 /www/wwwroot/resource_site/wp-content/themes/')
print(out)

# 2. Check current active theme
print('\n=== Current active theme ===')
out, _ = run_cmd(client, "cd /www/wwwroot/resource_site && wp option get template --allow-root 2>/dev/null || grep -o \"current_theme.*\" wp-config.php 2>/dev/null || echo 'wp-cli not available'")
print(out)

# Check DB directly
out, _ = run_cmd(client, """cd /www/wwwroot/resource_site && php -r "
define('ABSPATH', dirname(__FILE__).'/');
require_once 'wp-load.php';
echo 'template: ' . get_option('template') . \"\\n\";
echo 'stylesheet: ' . get_option('stylesheet') . \"\\n\";
echo 'current_theme: ' . wp_get_theme()->get('Name') . \"\\n\";
" 2>&1""")
print(out)

client.close()
