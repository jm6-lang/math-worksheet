import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

sftp = client.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\custom_style.css',
         '/www/wwwroot/resource_site/wp-content/themes/puock/assets/custom.css')
sftp.close()
print('CSS uploaded OK')

# Check theme functions.php for where to add CSS enqueue
stdin, stdout, stderr = client.exec_command(
    'cat /www/wwwroot/resource_site/wp-content/themes/puock/functions.php | python3 -c "import sys; lines=sys.stdin.readlines(); [print(i+1, l.rstrip()) for i,l in enumerate(lines) if \'wp_enqueue\' in l or \'add_action\' in l and \'enqueue\' in l]"',
    timeout=10
)
print('Enqueue lines:')
print(stdout.read().decode('utf-8', errors='replace'))
print(stderr.read().decode('utf-8', errors='replace'))

client.close()
