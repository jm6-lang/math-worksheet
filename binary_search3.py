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

# The files loaded by inc.php in order:
# 1. inc/dependent
# 2. vendor/autoload
# 3. inc/class/class
# 4. inc/code/require
# 5. inc/codestar-framework/codestar-framework
# 6. inc/widgets/widget-class
# 7. inc/options/options
# 8. inc/functions/functions
# 9. inc/widgets/widget-index
# 10. oauth/oauth
# 11. zibpay/functions
# 12. action/function
# 13. inc/functions/rest-api/function
# 14. inc/csf-framework/classes/zib-csf.class

# Binary search: test loading first N files
# We'll create a PHP script that loads WP then includes specific files

all_files = [
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

# Test each file individually with PHP CLI
# First, restore the original functions.php (with inc.php included)
run_cmd('cp /tmp/zibll_functions_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/functions.php')

# Create a custom inc.php that only loads files we specify
def create_test_inc(files_to_include, label):
    lines = ['<?php']
    lines.append('// Test inc.php - ' + label)
    lines.append('')
    for f in files_to_include:
        lines.append(f"echo 'Loading {f}...'; flush();")
        lines.append(f"require_once get_theme_file_path('{f}.php');")
        lines.append(f"echo ' OK\\n'; flush();")
    lines.append("echo 'ALL_DONE\\n';")
    
    content = '\n'.join(lines)
    sftp = client.open_sftp()
    with sftp.file('/tmp/test_inc.php', 'w') as fh:
        fh.write(content)
    sftp.close()
    
    # Copy to theme dir as inc.php
    run_cmd('cp /tmp/test_inc.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')

print('=== Binary Search: Testing file groups ===')
print()

# Test first 7 files (before inc/code/require)
create_test_inc(all_files[:3], 'first3')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Files 1-3 (dependent, autoload, class): {out[:500]}')

create_test_inc(all_files[:4], 'first4')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Files 1-4 (+ code/require): {out[:500]}')

# The hang is likely in code/require. Let's test files 5-14 without 4
create_test_inc(all_files[:3] + all_files[4:7], 'skip4_5to7')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Files 1-3,5-7 (skip code/require): {out[:500]}')

# If 1-3,5-7 works, try 1-3,5-8
create_test_inc(all_files[:3] + all_files[4:8], 'skip4_5to8')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Files 1-3,5-8 (skip code/require): {out[:500]}')

# Try 1-3,5-9
create_test_inc(all_files[:3] + all_files[4:10], 'skip4_5to10')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Files 1-3,5-10 (skip code/require): {out[:500]}')

# Try 1-3,5-14 (all except code/require)
create_test_inc(all_files[:3] + all_files[4:], 'skip4_all_rest')
out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=15)
print(f'Files 1-3,5-14 (all except code/require): {out[:500]}')

client.close()