import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 1. Fix wp-config.php - remove duplicate WP_DEBUG lines
fix_config = r"""sed -i '26,28d' /www/wwwroot/resource_site/wp-config.php"""
stdin, stdout, stderr = ssh.exec_command(fix_config)
# Actually let's be more careful - read the file first
stdin, stdout, stderr = ssh.exec_command("grep -n 'WP_DEBUG' /www/wwwroot/resource_site/wp-config.php")
debug_lines = stdout.read().decode('utf-8', errors='replace').strip()
print("WP_DEBUG lines: " + debug_lines, flush=True)

# Remove lines 27-29 (duplicate WP_DEBUG_LOG, WP_DEBUG_DISPLAY, empty line)
# Line 26: define('WP_DEBUG', true);     <- KEEP
# Line 27: define('WP_DEBUG_LOG', true);  <- REMOVE (dup)  
# Line 28: define('WP_DEBUG_DISPLAY', true); <- REMOVE (dup)
# Line 29: define('WP_DEBUG_LOG', true);  <- KEEP
# Line 30: define('WP_DEBUG_DISPLAY', false); <- KEEP
stdin, stdout, stderr = ssh.exec_command("sed -i '27,28d' /www/wwwroot/resource_site/wp-config.php")
# Verify
stdin, stdout, stderr = ssh.exec_command("grep -n 'WP_DEBUG' /www/wwwroot/resource_site/wp-config.php")
print("After fix: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# 2. Disable xenice-seo, activate wordpress-seo (Yoast)
stdin, stdout, stderr = ssh.exec_command("wp plugin deactivate xenice-seo --allow-root --path=/www/wwwroot/resource_site/ 2>&1")
print("Deactivate xenice: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

stdin, stdout, stderr = ssh.exec_command("wp plugin activate wordpress-seo --allow-root --path=/www/wwwroot/resource_site/ 2>&1")
print("Activate Yoast: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# 3. Check if Yoast was ever configured
stdin, stdout, stderr = ssh.exec_command("wp option get blogname --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null")
print("Blog name: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

stdin, stdout, stderr = ssh.exec_command("wp option get blogdescription --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null")
print("Blog desc: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# 4. Clear wp-super-cache
stdin, stdout, stderr = ssh.exec_command("wp super-cache flush --allow-root --path=/www/wwwroot/resource_site/ 2>&1 || echo 'wp-super-cache-not-installed'")
print("Cache flush: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# Clear all cache files
stdin, stdout, stderr = ssh.exec_command("rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/* 2>/dev/null && echo 'cache-files-cleared'")
print(stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

import time
time.sleep(2)

# 5. Test sitemap
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/sitemap_index.xml' 2>/dev/null | head -10")
print("Sitemap: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# 6. Test footer
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?nocache=5' 2>/dev/null | grep -c 'sitemap'")
print("Footer sitemap count: " + stdout.read().decode().strip(), flush=True)

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?nocache=5' 2>/dev/null | tail -c 300")
print("Footer area: " + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

ssh.close()
