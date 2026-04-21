import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Download functions.php to local
sftp = ssh.open_sftp()
sftp.get('/www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php', 'C:/Users/Administrator/.qclaw/workspace-agent-3bb7b585/functions.php')
sftp.close()

ssh.close()
print("Downloaded functions.php")
