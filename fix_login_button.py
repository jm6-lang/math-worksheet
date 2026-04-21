import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Find and replace the login buttons in header.php to add proper data-toggle and data-target
# Also add id="login-trigger" to the buttons

# First backup
stdin, stdout, stderr = ssh.exec_command(
    "cp /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php.bak2",
    timeout=10
)
print("Backup done")

# Replace the login buttons - add id="login-trigger" 
# The mobile sidebar button
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's/<button class=\"btn-register login-btn\">/<button class=\"btn-register login-btn\" id=\"login-trigger\" data-toggle=\"modal\" data-target=\"#login-modal\">/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Mobile button updated")

# The desktop header button
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's/<button class=\"btn btn-danger btn-sm login-btn/<button id=\"login-trigger\" class=\"btn btn-danger btn-sm login-btn/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Desktop button updated")

# Also add data-toggle and data-target to desktop button
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's/<button id=\"login-trigger\" class=\"btn btn-danger btn-sm login-btn/<button id=\"login-trigger\" data-toggle=\"modal\" data-target=\"#login-modal\" class=\"btn btn-danger btn-sm login-btn/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Desktop button data attributes added")

# Verify changes
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'login-btn\\|login-trigger' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print('\nChanges:', stdout.read().decode('utf-8', errors='replace'))

ssh.close()
print("\nDone! Login buttons should now work.")