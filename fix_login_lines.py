import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Restore from backup again
stdin, stdout, stderr = ssh.exec_command(
    "cp /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php.bak2 /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Restored")

# Show current lines for both buttons
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '38p;73p' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print('Current lines:', stdout.read().decode('utf-8', errors='replace'))

# Mobile button (line 38): <button class="btn-register login-btn">
stdin, stdout, stderr = ssh.exec_command(
    "sed -i '38s/<button class=\"btn-register login-btn\">/<button class=\"btn-register login-btn\" data-toggle=\"modal\" data-target=\"#login-modal\">/' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Fixed line 38")

# Desktop button (line 73): <button class="btn btn-danger btn-sm login-btn d-none d-md-block"
# We need to add data-toggle and data-target AFTER the class attribute but before d-none
stdin, stdout, stderr = ssh.exec_command(
    "sed -i '73s/login-btn d-none/login-btn\" data-toggle=\"modal\" data-target=\"#login-modal\" d-none/' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Fixed line 73")

# Verify
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '38p;73p' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print('\nFixed lines:', stdout.read().decode('utf-8', errors='replace'))

ssh.close()