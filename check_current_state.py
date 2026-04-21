import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Retry connection
for attempt in range(3):
    try:
        client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
        break
    except Exception as e:
        print(f'Attempt {attempt+1} failed: {e}')
        time.sleep(3)

print('[FIX] Connected')

# Use exec only (no SFTP for large files)

# Step 1: Fix code.php - replace curl_update and is_update functions using sed
# First, let's check the file state
stdin, stdout, stderr = client.exec_command('grep -n "function curl_update\\|function is_update\\|function is_aut" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php 2>/dev/null')
print('Functions:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

# Step 2: Check if options-module.php is fixed
stdin, stdout, stderr = client.exec_command('grep -c "ZibAut::is_update" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php 2>/dev/null')
count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'options-module.php is_update count: {count}')

# Step 3: Check admin-options.php
stdin, stdout, stderr = client.exec_command('grep -c "ZibAut::is_update" /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php 2>/dev/null')
count2 = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'admin-options.php is_update count: {count2}')

# Step 4: The white page issue - let's use PHP to fix code.php
# Instead of modifying the obfuscated file, let's add a mu-plugin that 
# defines wrapper functions BEFORE code.php loads

# Actually, the problem might be that code.php itself crashes during class definition
# Let's check: does the white page happen on frontend or only admin?

stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/ 2>&1')
home = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage: {home}')

stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | wc -c')
home_size = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage size: {home_size} bytes')

stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | head -1')
home_start = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Homepage start: {home_start[:200]}')

stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/wp-login.php 2>&1')
login = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Login: {login}')

stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/wp-login.php 2>&1 | head -1')
login_start = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Login start: {login_start[:200]}')

client.close()