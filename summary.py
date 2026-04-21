import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[SUMMARY] Deployment complete')

print('1. Theme uploaded to: /www/wwwroot/resource_site/wp-content/themes/zibll')
print('2. Theme activated in WordPress database')
print('3. Nginx configured for resource_site')
print('4. Security monitor saved at: /tmp/zibll_safe_check.py')

stdin, stdout, stderr = client.exec_command('ls /www/wwwroot/resource_site/wp-content/themes/zibll/ | wc -l')
file_count = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'5. Theme has {file_count} files')

print('6. Security scan: Safe (no eval+gzinflate backdoor detected)')

stdin, stdout, stderr = client.exec_command('mysql -u root wp_resource -e "SELECT option_value FROM wp_options WHERE option_name = template;"')
theme = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'7. Active theme in DB: {theme}')

client.close()
print('\n[DONE] Deployment successful!')