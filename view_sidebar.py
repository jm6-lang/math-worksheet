import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Read sidebar.php around line 24
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '15,40p' /www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar.php",
    timeout=10
)
print("Sidebar tag cloud section:")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()