import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Find zib_footer_conter hook')

# Search for zib_footer_conter in theme files
stdin, stdout, stderr = client.exec_command("grep -rn 'zib_footer_conter\\|footer_conter' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>/dev/null | head -20")
print('Hook references:', stdout.read().decode('utf-8', errors='ignore').strip())

# Search for where footer content is actually rendered
stdin, stdout, stderr = client.exec_command("grep -rn 'footer_t1\\|fcode_t1\\|fcode_t2' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' 2>/dev/null | head -20")
print('Footer content keys:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()