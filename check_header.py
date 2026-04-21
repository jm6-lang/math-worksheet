import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Get current site URL from database
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT option_name, option_value FROM wp_options WHERE option_name IN (\"siteurl\",\"home\")' 2>/dev/null",
    timeout=10
)
print('Site URLs in DB:', stdout.read().decode('utf-8', errors='replace').strip())

# List themes
stdin, stdout, stderr = ssh.exec_command(
    "ls /www/wwwroot/resource_site/wp-content/themes/",
    timeout=10
)
print('Themes dir:', stdout.read().decode('utf-8', errors='replace').strip())

# Get header.php from active theme
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php | head -120",
    timeout=10
)
print('\nHeader.php:\n', stdout.read().decode('utf-8', errors='replace'))

ssh.close()
