import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Prevent ZibAut::is_update from being called')

# The issue is in admin-options.php line 11090: ZibAut::is_update()
# Let me disable that call specifically

# Read admin-options.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

lines = content.split('\n')

# Find line 11090
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\admin_opts_11090.txt', 'w', encoding='utf-8') as out:
    for i in range(11085, min(11100, len(lines))):
        out.write(f'{i+1}: {lines[i]}\n')

print('Saved admin-options.php around line 11090')

# Find the exact call and comment it out
target_lines = []
for i, line in enumerate(lines):
    if 'ZibAut::is_update' in line or 'is_update()' in line:
        target_lines.append(i+1)
        print(f'Found is_update call at line {i+1}: {line.strip()[:100]}')

# Also check for csf_zibll_options_save_before hook
for i, line in enumerate(lines):
    if 'csf_zibll_options_save_before' in line:
        print(f'Found save hook at line {i+1}: {line.strip()[:100]}')

client.close()