import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check the theme's JS files for login handling
stdin, stdout, stderr = ssh.exec_command(
    "grep -r 'login-btn\\|login' /www/wwwroot/resource_site/wp-content/themes/yymarket/*.js 2>/dev/null | head -20",
    timeout=10
)
print('JS login refs:', stdout.read().decode('utf-8', errors='replace').strip())

# Check footer for any login-related code
stdin, stdout, stderr = ssh.exec_command(
    "grep -i 'login\\|register\\|wp-login' /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php 2>/dev/null | head -10",
    timeout=10
)
print('Footer login refs:', stdout.read().decode('utf-8', errors='replace').strip())

# Check if there's a custom JS
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/wp-content/themes/yymarket/assets/js/ 2>/dev/null || ls -la /www/wwwroot/resource_site/wp-content/themes/yymarket/js/ 2>/dev/null",
    timeout=10
)
print('JS files:', stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
