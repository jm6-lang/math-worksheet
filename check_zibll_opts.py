import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[BEAUTIFY] Configure Zibll theme')

# Step 1: Check current zibll_options
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT LENGTH(option_value) FROM wp_skillxm.wp_options WHERE option_name = 'zibll_options';\"")
opt_len = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'zibll_options size: {opt_len}')

# Step 2: Get current zibll_options content (just first part to understand structure)
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT SUBSTRING(option_value, 1, 500) FROM wp_skillxm.wp_options WHERE option_name = 'zibll_options';\"")
opt_preview = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'zibll_options preview: {opt_preview}')

# Step 3: Check theme_mods_zibll
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"SELECT option_value FROM wp_skillxm.wp_options WHERE option_name = 'theme_mods_zibll';\"")
mods = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'theme_mods_zibll: {mods[:500]}')

client.close()