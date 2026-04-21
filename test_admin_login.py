import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[TEST] wp-admin login test')

# Login first
stdin, stdout, stderr = client.exec_command('curl -s -k -c /tmp/test_cookies -b /tmp/test_cookies -L -d "log=admin&pwd=Admin123456&wp-submit=Log+In&redirect_to=https%3A%2F%2F127.0.0.1%2Fwp-admin%2F&testcookie=1" "https://127.0.0.1/wp-login.php" -o /tmp/test_login.html -w "%{http_code}" 2>&1')
login_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Login HTTP: {login_code}')

# Check for errors in login result
stdin, stdout, stderr = client.exec_command('grep -c "Fatal\\|Error\\|error" /tmp/test_login.html 2>/dev/null')
errs = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Login page errors: {errs}')

# Check for dashboard
stdin, stdout, stderr = client.exec_command('grep -c "dashboard" /tmp/test_login.html 2>/dev/null')
dash = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Dashboard found: {dash}')

# Access wp-admin after login
stdin, stdout, stderr = client.exec_command('curl -s -k -b /tmp/test_cookies "https://127.0.0.1/wp-admin/" -o /tmp/test_admin.html -w "%{http_code}" 2>&1')
admin_code = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'wp-admin after login: {admin_code}')

# Check for fatal errors
stdin, stdout, stderr = client.exec_command('grep -c "Fatal\\|database error" /tmp/test_admin.html 2>/dev/null')
fatal = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Fatal errors in admin: {fatal}')

client.close()