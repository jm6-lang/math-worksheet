import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check for login-btn click handler
stdin, stdout, stderr = ssh.exec_command(
    "grep -r 'login-btn\\|#login-modal' /www/wwwroot/resource_site/wp-content/themes/yymarket/ 2>/dev/null | grep -v 'Binary'",
    timeout=10
)
print('Login button refs:', stdout.read().decode('utf-8', errors='replace').strip())

# Check where the modal is loaded/printed
stdin, stdout, stderr = ssh.exec_command(
    "grep -r 'login-modal\\|user-login' /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php 2>/dev/null",
    timeout=10
)
print('\nModal refs:', stdout.read().decode('utf-8', errors='replace').strip())

# Check footer for modal output
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'wp_footer\\|do_action' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php 2>/dev/null",
    timeout=10
)
print('\nFooter actions:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()