import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[DEBUG] Check current error')

stdin, stdout, stderr = client.exec_command('tail -5 /var/log/nginx/error.log')
print('Nginx:', stdout.read().decode('utf-8', errors='ignore').strip()[:600])

# Check PHP error
stdin, stdout, stderr = client.exec_command('grep -i "error\\|parse\\|syntax" /tmp/test_admin3.html 2>/dev/null | head -3')
print('Admin HTML errors:', stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# Restore from backup and try a different approach
print('\n[RESTORE] Restore original code.php and try different approach')
stdin, stdout, stderr = client.exec_command('cp /tmp/themes_backup/inc/code/code.php /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php')
print('Restored code.php from backup')

# Instead of patching, lets try adding a must-use plugin to disable update checks
mu_plugin = """<?php
// Disable Zibll update/authorization checks
add_action('init', function() {
    // Remove the admin update check hooks
    remove_all_actions('admin_init');
    remove_all_actions('admin_head');
}, 999);

// Override ZibAut class if it exists
if (class_exists('ZibAut')) {
    // Replace methods via monkey-patching
}
""";

f = sftp.file('/tmp/restore_backup.php', 'w')
f.write('')

# Actually, let me just check what new_aut.php does
stdin, stdout, stderr = client.exec_command('head -20 /www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/new_aut.php')
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\new_aut.txt', 'w', encoding='utf-8') as out:
    out.write(stdout.read().decode('utf-8', errors='replace'))
print('Saved new_aut.php')

client.close()