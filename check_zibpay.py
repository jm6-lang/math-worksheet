import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Zibpay tables situation')

# List tables in wp_skillxm
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_skillxm;"')
all_tables = stdout.read().decode('utf-8', errors='ignore').strip()
print('All tables in wp_skillxm:')
for line in all_tables.split('\n')[1:]:
    if 'zibpay' in line.lower():
        print(f'  ZIBPAY: {line}')

# Check wp_resource for zibpay tables
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SHOW TABLES FROM wp_resource;"')
res_tables = stdout.read().decode('utf-8', errors='ignore').strip()
print('\nZibpay in wp_resource:')
for line in res_tables.split('\n')[1:]:
    if 'zibpay' in line.lower():
        print(f'  {line}')

# Count total tables
print('\nTotal tables in wp_skillxm:', len(all_tables.split('\n')) - 1)

client.close()
print('[DONE]')