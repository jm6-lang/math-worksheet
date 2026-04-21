import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[CHECK] Find Zibll footer config keys')

# Read admin-options.php to find footer copyright key
stdin, stdout, stderr = client.exec_command("grep -n 'footer\\|copyright\\|版权\\|run_time\\|safe_run\\|beian' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php | head -30")
print('Footer related keys:', stdout.read().decode('utf-8', errors='ignore').strip()[:1000])

# Also check the footer widgets output
stdin, stdout, stderr = client.exec_command("grep -rn 'do_action.*footer\\|wp_footer\\|all_footer' /www/wwwroot/resource_site/wp-content/themes/zibll/ --include='*.php' | head -10")
print('Footer hooks:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()