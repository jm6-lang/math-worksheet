import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Read archive.php pagination area
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '40,80p' /www/wwwroot/resource_site/wp-content/themes/yymarket/archive.php", timeout=10)
print('=== archive.php (lines 40-80) ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Read home-1.php pagination area
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '100,135p' /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php", timeout=10)
print('\n=== home-1.php (lines 100-135) ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Read index.php pagination area
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '70,100p' /www/wwwroot/resource_site/wp-content/themes/yymarket/index.php", timeout=10)
print('\n=== index.php (lines 70-100) ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check existing pagination CSS
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'pagination' /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css", timeout=10)
print('\n=== Pagination in custom.css ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check main style.css for pagination
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'pagination' /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css | head -20", timeout=10)
print('\n=== Pagination in style.css ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check for ad units
stdin, stdout, stderr = ssh.exec_command(
    "grep -rn 'adsense\\|adsbygoogle\\|ad-slot\\|ins class' /www/wwwroot/resource_site/wp-content/themes/yymarket/ --include='*.php' | head -20", timeout=10)
print('\n=== Ad units ===')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
