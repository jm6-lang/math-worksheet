import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Read the exact line 21
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '21p' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
line21 = stdout.read().decode().strip()
print(f"Line 21: {repr(line21)}")

# Fix it properly - replace the whole line
stdin, stdout, stderr = ssh.exec_command(
    "sed -i '21s/.*/        if (!function_exists(\"is_product\") || !is_product()) {/' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("Fixed line 21")

# Verify
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '21p' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("After fix:", stdout.read().decode().strip())

ssh.close()