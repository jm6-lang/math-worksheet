import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Login and check errors')

# Check login page content
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php" | grep -i "error\\|Error\\|FATAL" | head -5')
print('Login page errors:', stdout.read().decode('utf-8', errors='ignore').strip())

# Check if registration works
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php?action=register" | head -20')
reg_page = stdout.read().decode('utf-8', errors='ignore').strip()
print('Register page:', reg_page[:300])

# Check if users_can_register is set
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT option_value FROM wp_skillxm.wp_options WHERE option_name = 'users_can_register';\"")
reg = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Registration enabled: {reg}')

# Check PHP errors
stdin, stdout, stderr = client.exec_command('tail -10 /var/log/nginx/error.log')
print('Recent nginx errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()