import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Restore from backup
stdin, stdout, stderr = ssh.exec_command(
    "cp /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php.bak2 /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Restored")

# Read the whole file and do precise replacement
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
content = stdout.read().decode('utf-8', errors='replace')

# Replace mobile button
content = content.replace(
    '<button class="btn-register login-btn">',
    '<button class="btn-register login-btn" data-toggle="modal" data-target="#login-modal">'
)

# Replace desktop button
content = content.replace(
    '<button class="btn btn-danger btn-sm login-btn d-none d-md-block"',
    '<button class="btn btn-danger btn-sm login-btn d-none d-md-block" data-toggle="modal" data-target="#login-modal"'
)

# Write back
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/header.php', 'w') as f:
    f.write(content)
sftp.close()

# Verify
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'login-btn' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print('Fixed:', stdout.read().decode('utf-8', errors='replace'))

ssh.close()
print("Done!")