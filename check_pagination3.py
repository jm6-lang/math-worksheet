import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Read current pagination CSS rules
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '148,185p' /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css", timeout=10)
print('=== Current pagination CSS ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check what the actual pagination HTML looks like on a page
stdin, stdout, stderr = ssh.exec_command(
    "curl -s https://www.skillxm.cn/ | grep -oP '<ul class=\"pagination\">.*?</ul>' | head -3", timeout=15)
print('\n=== Pagination HTML from homepage ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check the full home-1.php to see if there are inline ad slots
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php | wc -l", timeout=10)
print('\n=== home-1.php total lines ===')
print(stdout.read().decode().strip())

# Check archive.php fully
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/archive.php", timeout=10)
print('\n=== archive.php full ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check for any existing mobile ad placement
stdin, stdout, stderr = ssh.exec_command(
    "grep -rn 'adsbygoogle\\|ad-slot\\|data-ad' /www/wwwroot/resource_site/wp-content/themes/yymarket/ --include='*.php' --include='*.css' --include='*.js' 2>/dev/null", timeout=10)
print('\n=== All ad references ===')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
