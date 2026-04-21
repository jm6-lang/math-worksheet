import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check the problematic file
stdin, stdout, stderr = ssh.exec_command(
    "sed -n '15,30p' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("Line 21 context:")
print(stdout.read().decode('utf-8', errors='replace'))

# Check if WooCommerce is active
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp plugin is-active woocommerce --allow-root 2>&1 || echo 'WooCommerce not active'",
    timeout=15
)
print("\nWooCommerce status:", stdout.read().decode().strip())

# Quick fix: wrap is_product() check with function_exists
stdin, stdout, stderr = ssh.exec_command(
    """sed -i 's/if ( is_product()/if ( function_exists(\"is_product\") \&\& is_product()/g' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php""",
    timeout=10
)
print("\nApplied fix")

# Verify
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'is_product' /www/wwwroot/resource_site/wp-content/plugins/xenice-member/includes/class-wc-free-download.php",
    timeout=10
)
print("After fix:", stdout.read().decode().strip())

ssh.close()
print("\nDone! Try refreshing the site.")