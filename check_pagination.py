import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# 1. Find pagination templates
stdin, stdout, stderr = ssh.exec_command(
    "grep -rn 'pagination\\|nav-links\\|page-numbers\\|paging' /www/wwwroot/resource_site/wp-content/themes/yymarket/ --include='*.php' | head -30"
    , timeout=10)
print('=== Pagination refs ===')
print(stdout.read().decode('utf-8', errors='replace'))

# 2. Find archive/product listing template
stdin, stdout, stderr = ssh.exec_command(
    "find /www/wwwroot/resource_site/wp-content/themes/yymarket/ -name '*.php' | xargs grep -l 'pagination\\|nav-links' | head -10"
    , timeout=10)
print('=== Files with pagination ===')
print(stdout.read().decode('utf-8', errors='replace'))

# 3. Check the pagination function
stdin, stdout, stderr = ssh.exec_command(
    "grep -rn 'function.*pagination\\|the_posts_pagination\\|paginate_links' /www/wwwroot/resource_site/wp-content/themes/yymarket/ --include='*.php' | head -20"
    , timeout=10)
print('=== Pagination functions ===')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
