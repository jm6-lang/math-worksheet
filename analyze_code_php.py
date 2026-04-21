import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('[FIX] Fix Zibll code.php')

# First restore code.php from backup
stdin, stdout, stderr = client.exec_command('cp /tmp/themes_backup/inc/code/code.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php')
print('Restored code.php from backup')

# Check syntax
stdin, stdout, stderr = client.exec_command('php -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php 2>&1')
print('Syntax:', stdout.read().decode('utf-8', errors='ignore').strip())

# Read code.php content
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

# Find the ZibAut class - we need to find where it defines the class and its methods
# The class definition starts at around line 290
# We need to check what happens during class definition (not method calls)
# In PHP, class properties and method definitions are parsed at load time
# But eval() in property initializers or __construct would execute at instantiation

# Let's find the class definition and see if there's anything that runs at load time
lines = content.split('\n')

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\code_php_analysis.txt', 'w', encoding='utf-8') as out:
    # Show lines 1-30 and 285-310
    for i in range(0, 30):
        out.write(f'{i+1}: {lines[i]}\n')
    out.write('\n--- CLASS AREA ---\n')
    for i in range(284, min(320, len(lines))):
        out.write(f'{i+1}: {lines[i]}\n')
    
    # Also check new_aut.php line 15
    out.write('\n--- new_aut.php ---\n')

print('Saved analysis')

# Check new_aut.php
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php', 'r')
new_aut = f.read().decode('utf-8', errors='replace')
f.close()

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\code_php_analysis.txt', 'a', encoding='utf-8') as out:
    out.write(new_aut[:1000])

# Check if new_aut.php line 15 is commented out
stdin, stdout, stderr = client.exec_command('head -20 /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php')
print('new_aut.php:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

client.close()