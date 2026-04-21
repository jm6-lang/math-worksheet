import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check how login is hooked into WordPress
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'add_action\\|add_shortcode' /www/wwwroot/resource_site/wp-content/themes/yymarket/vessel/login/Login.php | head -20",
    timeout=10
)
print('Login hooks:', stdout.read().decode('utf-8', errors='replace').strip())

# Check if wp_footer is being used to output the modal
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'wp_footer\\|footer\\|print' /www/wwwroot/resource_site/wp-content/themes/yymarket/vessel/login/Login.php | head -10",
    timeout=10
)
print('\nFooter refs:', stdout.read().decode('utf-8', errors='replace').strip())

# Check if there's an init or other hook
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'function\\|add_' /www/wwwroot/resource_site/wp-content/themes/yymarket/vessel/login/Login.php | head -30",
    timeout=10
)
print('\nFunctions:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()