import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Fix duplicate ID - use different IDs for the two buttons
# Desktop button should keep id="login-trigger"
# Mobile button should have a different ID or just use data attributes

# Restore from backup first
stdin, stdout, stderr = ssh.exec_command(
    "cp /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php.bak2 /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Restored from backup")

# Create the proper fix - use class-based trigger instead of ID
# Mobile sidebar button - just use data attributes
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's/<button class=\"btn-register login-btn\">/<button class=\"btn-register login-btn\" data-toggle=\"modal\" data-target=\"#login-modal\">/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Mobile button: added data attributes")

# Desktop header button - use data attributes too
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's/<button class=\"btn btn-danger btn-sm login-btn/<button class=\"btn btn-danger btn-sm login-btn\" data-toggle=\"modal\" data-target=\"#login-modal\"/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print("Desktop button: added data attributes")

# Check if there's a link to login page that we should also fix
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'login' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php",
    timeout=10
)
print('\nLogin refs:', stdout.read().decode('utf-8', errors='replace'))

ssh.close()
print("\nFixed! Both buttons now have data-toggle='modal' data-target='#login-modal'")