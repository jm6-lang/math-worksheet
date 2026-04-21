import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Fix the xenice-member plugin
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '20,25p' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("Current line 21:")
print(stdout.read().decode())

# Apply fix - wrap is_product() with function_exists check
stdin, stdout, stderr = ssh.exec_command(
    "sed -i 's/if (!is_product())/if (!function_exists(\"is_product\") || !is_product())/g' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("Fix applied")

# Verify fix
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '20,25p' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("\nAfter fix:")
print(stdout.read().decode())

# Restart PHP-FPM
stdin, stdout, stderr = ssh.exec_command("systemctl restart php8.1-fpm && echo 'PHP-FPM restarted'", timeout=15)
print(stdout.read().decode())

# Test site
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' -H 'Host: skillxm.cn' https://127.0.0.1/", timeout=15)
print("\nSite HTTP status:", stdout.read().decode().strip())

ssh.close()
print("\nDone!")
