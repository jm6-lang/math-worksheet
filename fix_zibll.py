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

# Step 1: Backup inc.php
run_cmd('cp /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php /tmp/inc_php_backup.php')
print('Backed up inc.php')

# Step 2: Comment out the problematic file from the require list
# Replace 'inc/code/require', with '// BLOCKED: inc/code/require',
cmd = r"""sed -i "s/    'inc\/code\/require',$/    \/\/ BLOCKED: 'inc\/code\/require',/" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php"""
run_cmd(cmd)
print('Commented out inc/code/require in inc.php')

# Verify
out = run_cmd("grep -n 'code/require\\|BLOCKED' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php")
print(f'Verify: {out}')

# Step 3: Switch to Zibll theme
run_cmd("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'zibll' WHERE option_name IN ('template', 'stylesheet');\"")
print('Switched to Zibll theme')

# Step 4: Restart PHP-FPM
run_cmd('systemctl restart php8.1-fpm')
time.sleep(2)
print('Restarted PHP-FPM')

# Step 5: Test
print('\n=== Testing site ===')
out = run_cmd('curl -s -k --max-time 10 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/ 2>&1')
print(f'Frontend: {out}')

out = run_cmd('curl -s -k --max-time 10 -o /dev/null -w "HTTP %{http_code}, Size %{size_download}" https://127.0.0.1/wp-login.php 2>&1')
print(f'Login: {out}')

# Step 6: If it works, check if there are any fatal errors
out = run_cmd('curl -s -k --max-time 10 https://127.0.0.1/ 2>&1 | grep -i "fatal\|error\|warning" | head -5')
if out:
    print(f'Errors found: {out[:500]}')
else:
    print('No obvious PHP errors on frontend')

client.close()