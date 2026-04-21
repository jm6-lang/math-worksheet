import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[TEST] Full wp-admin functionality')

# Step 1: Login to wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k -c /tmp/wp_cookie.txt "https://127.0.0.1/wp-login.php" > /dev/null 2>&1')

# Login POST
stdin, stdout, stderr = client.exec_command('curl -s -k -c /tmp/wp_cookie.txt -b /tmp/wp_cookie.txt -L -d "log=admin&pwd=Admin123456&wp-submit=Log+In&redirect_to=https%3A%2F%2F127.0.0.1%2Fwp-admin%2F&testcookie=1" "https://127.0.0.1/wp-login.php" -o /tmp/wp_login_result.html 2>&1')

# Check login result
stdin, stdout, stderr = client.exec_command('grep -c "dashboard" /tmp/wp_login_result.html 2>/dev/null')
dash_count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Dashboard match: {dash_count}')

# Check for errors
stdin, stdout, stderr = client.exec_command('grep -c "Error\\|error\\|Fatal" /tmp/wp_login_result.html 2>/dev/null')
err_count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Errors in login: {err_count}')

# Step 2: Check if we can access theme options page
stdin, stdout, stderr = client.exec_command('curl -s -k -b /tmp/wp_cookie.txt "https://127.0.0.1/wp-admin/admin.php?page=zibll_options" -o /tmp/zibll_opts.html 2>&1')
stdin, stdout, stderr = client.exec_command('grep -c "theme-options\\|zibll\\|Zibll" /tmp/zibll_opts.html 2>/dev/null')
zibll_count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Zibll options page match: {zibll_count}')

# Step 3: Check current homepage title
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ | grep -oP "<title>.*?</title>"')
title = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Current homepage title: {title}')

client.close()
print('[DONE]')