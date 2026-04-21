import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Disable Zibll auto-update check')

# Check the code.php around line 373
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

lines = content.split('\n')

# Find ZibAut::is_update() or curl_update calls
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\code_aut.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines):
        if 'is_update' in line or 'is_aut' in line or 'ZibAut' in line or 'curl_update' in line:
            out.write(f'{i+1}: {line.strip()[:150]}\n')

print('Saved references')

# Check if there's a way to mark it as authorized
for i, line in enumerate(lines):
    if 'is_local' in line or 'is_localhost' in line:
        print(f'Local check at line {i+1}: {line.strip()[:150]}')

client.close()