import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Footer area context around line 2762')

# Read lines 2730-2820 of admin-options.php
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

lines = content.split('\n')
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\admin_opts_footer.txt', 'w', encoding='utf-8') as out:
    for i in range(2729, min(2830, len(lines))):
        out.write(f'{i+1}: {lines[i]}\n')

print('Saved to local file')

# Also get lines around 5353 for the footer main setting
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\admin_opts_footer.txt', 'a', encoding='utf-8') as out:
    out.write('\n--- Around line 5353 ---\n')
    for i in range(5345, min(5380, len(lines))):
        out.write(f'{i+1}: {lines[i]}\n')

client.close()