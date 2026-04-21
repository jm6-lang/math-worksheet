import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/header.php', 'r') as f:
    content = f.read().decode('utf-8', errors='replace')
print(content)
sftp.close()
ssh.close()
