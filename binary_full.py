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

def test_with_disabled(disabled_files, label, timeout=12):
    """Restore inc.php, comment out specified files, test"""
    run_cmd('cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')
    
    patch_script = "path = '/www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php'\n"
    patch_script += "with open(path, 'r', encoding='utf-8', errors='replace') as f:\n"
    patch_script += "    content = f.read()\n"
    for df in disabled_files:
        patch_script += f"content = content.replace(\"    '{{df}}',\", \"    // '{{df}}', // DISABLED\", 1)\n"
    patch_script += "with open(path, 'w', encoding='utf-8') as f:\n"
    patch_script += "    f.write(content)\n"
    
    sftp = client.open_sftp()
    with sftp.file('/tmp/patch.py', 'w') as f:
        f.write(patch_script)
    sftp.close()
    run_cmd('python3 /tmp/patch.py')
    
    out = run_cmd('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 /tmp/test_wp_only.php 2>&1', timeout=timeout)
    status = 'OK' if 'WP_OK' in out else ('HANG' if not out else f'ERROR: {out[:200]}')
    print(f'  {label}: {status}')
    return status

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

# Already know: files 1-3 work, file 4 hangs
# Need to test files 5-14 individually

print('=== Testing files 5-14 individually (with 1-3 always enabled) ===')

# Test each file from index 4 onwards, with all previous working files
# We know 1-3 work, 4 hangs. 
# Test: 1-3 + 5, 1-3 + 6, etc.

for i in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
    enabled = all_files[:3] + [all_files[i]]
    disabled = [f for j, f in enumerate(all_files) if j not in list(range(3)) + [i]]
    test_with_disabled(disabled, f'{all_files[i]}')

print('\n=== Testing files 5-10 together (skip 4) ===')
disabled = [all_files[3]] + all_files[10:]
test_with_disabled(disabled, 'files 5-10 only')

print('\n=== Testing files 5-14 together (skip 4) ===')
disabled = [all_files[3]]
test_with_disabled(disabled, 'files 5-14 (all except code/require)')

# Restore original for safety
run_cmd('cp /tmp/inc_php_backup.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php')
print('\nRestored original inc.php')

client.close()