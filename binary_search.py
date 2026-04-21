import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

def run_cmd(cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        return out
    except:
        return '[TIMEOUT]'

# Show the full array from line 97
print('=== inc.php line 97-115 (file list) ===')
out = run_cmd("sed -n '97,115p' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>&1")
print(out)

# Check inc/code/require.php
print('\n=== inc/code/require.php ===')
out = run_cmd("cat /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/require.php 2>&1")
print(out[:2000])

# Now let's do binary search: load files one by one via PHP CLI
# We'll test each file individually with a timeout
print('\n=== Testing each file with 5s timeout ===')

files = [
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
]

for f in files:
    path = f'/www/wwwroot/resource_site/wp-content/themes/zibll/{f}.php'
    result = run_cmd(f'cd /www/wwwroot/resource_site && timeout 5 php -l {path} 2>&1')
    syntax_ok = 'No syntax errors' in result
    print(f'  {f}.php - syntax: {"OK" if syntax_ok else "ERROR"}')

# Binary search approach: load files incrementally
print('\n=== Binary search: load first N files ===')

# Test loading just the first 3 files
for n in [3, 4, 5]:
    cmd = f'''cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 -r "
    define('WP_USE_THEMES', false);
    define('ABSPATH', '/www/wwwroot/resource_site/');
    require_once ABSPATH . 'wp-load.php';
    echo 'WP loaded OK\\n';
    " 2>&1 | tail -5'''
    result = run_cmd(cmd, timeout=12)
    print(f'  First {n} files: {result[:300]}')

client.close()