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

def run_cmd(client, cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Test: how long does loading code.php take?
test_code = """<?php
// /tmp/test_code.php
$start = microtime(true);
require_once '/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php';
$elapsed = round((microtime(true) - $start) * 1000);
echo "code.php loaded in {$elapsed}ms\\n";
"""

sftp = client.open_sftp()
with sftp.file('/tmp/test_code.php', 'w') as f:
    f.write(test_code)
sftp.close()

print('=== How long does code.php take to load? ===')
out = run_cmd(client, 'timeout 10 php /tmp/test_code.php 2>&1', timeout=15)
print(f'Result: {out}')

# Test loading require.php from backup
test_require = """<?php
$start = microtime(true);
require_once '/tmp/themes_backup/inc/code/require.php';
$elapsed = round((microtime(true) - $start) * 1000);
echo "require.php loaded in {$elapsed}ms\\n";
"""
with sftp.file('/tmp/test_require.php', 'w') as f:
    f.write(test_require)
sftp.close()

print('\n=== How long does original require.php take? ===')
out = run_cmd(client, 'timeout 10 php /tmp/test_require.php 2>&1', timeout=15)
print(f'Result: {out}')

# The key question: does code.php itself hang, or does require.php hang?
# If code.php doesn't hang, we can just load code.php directly
# If require.php hangs but code.php doesn't, then require.php does something extra

# Test: load code.php with a 3 second timeout
print('\n=== code.php with 3s timeout ===')
out = run_cmd(client, 'timeout 3 php /tmp/test_code.php 2>&1', timeout=8)
print(f'Result: {out}')

client.close()