import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/class/card-pass.php', 'r')
content = f.read().decode('utf-8', errors='replace')
f.close()

# Save to local file for reading
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\card-pass.php', 'w', encoding='utf-8') as out:
    out.write(content)

# Also save order-class.php for reference
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/zibpay.disabled/class/order-class.php', 'r')
content2 = f.read().decode('utf-8', errors='replace')
f.close()
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\order-class.php', 'w', encoding='utf-8') as out:
    out.write(content2)

print('Files saved locally')

client.close()