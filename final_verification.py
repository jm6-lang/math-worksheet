import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('=' * 50)
print('FINAL SITE VERIFICATION')
print('=' * 50)

# Homepage
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | grep -oP "<title>.*?</title>"')
title = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Title: {title}')

# Footer content
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | grep -c "container-footer"')
footer = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'Footer present: {"Yes" if int(footer) > 0 else "No"}')

# Copyright
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | grep -c "ICP"')
icp = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'ICP info: {"Yes" if int(icp) > 0 else "No"}')

# Registration
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php?action=register" -o /dev/null -w "%{http_code}"')
print(f'Registration page: HTTP {stdout.read().decode("utf-8", errors="ignore").strip()}')

# wp-admin
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-admin/" -o /dev/null -w "%{http_code}"')
print(f'wp-admin: HTTP {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Login
stdin, stdout, stderr = client.exec_command('curl -s -k "https://127.0.0.1/wp-login.php" -o /dev/null -w "%{http_code}"')
print(f'Login page: HTTP {stdout.read().decode("utf-8", errors="ignore").strip()}')

# Theme
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT option_value FROM wp_skillxm.wp_options WHERE option_name = 'template';\"")
print(f'Active theme: {stdout.read().decode("utf-8", errors="ignore").strip().split(chr(10))[-1] if stdout.read().decode("utf-8", errors="ignore").strip() else "unknown"}')

# Zibpay tables
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT COUNT(*) FROM wp_skillxm.wp_zibpay_order;\"")
print(f'Zibpay order table rows: {stdout.read().decode("utf-8", errors="ignore").strip().split(chr(10))[-1]}')

# Nav menu
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT COUNT(*) FROM wp_skillxm.wp_terms WHERE term_id = 52;\"")
print(f'Nav menu exists: {stdout.read().decode("utf-8", errors="ignore").strip().split(chr(10))[-1]}')

print('=' * 50)

client.close()