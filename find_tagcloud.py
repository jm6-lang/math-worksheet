import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Find tag cloud / 标签云 in theme files
stdin, stdout, stderr = ssh.exec_command(
    "grep -rn '标签云\\|tag-cloud\\|wp_tag_cloud\\|wp_generate_tag_cloud' /www/wwwroot/resource_site/wp-content/themes/yymarket/ 2>/dev/null | head -20",
    timeout=15
)
print("Tag cloud references:", stdout.read().decode('utf-8', errors='replace'))

# Check category template
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/wp-content/themes/yymarket/category.php 2>/dev/null || echo 'No category.php'",
    timeout=10
)
print("\nCategory template:", stdout.read().decode().strip())

# Check archive template
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/wp-content/themes/yymarket/archive.php 2>/dev/null || echo 'No archive.php'",
    timeout=10
)
print("Archive template:", stdout.read().decode().strip())

# Check sidebar
stdin, stdout, stderr = ssh.exec_command(
    "grep -rn '标签云\\|tag-cloud' /www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar*.php 2>/dev/null",
    timeout=10
)
print("\nSidebar tag cloud:", stdout.read().decode('utf-8', errors='replace'))

ssh.close()