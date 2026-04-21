import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
s=paramiko.SSHClient(); s.set_missing_host_key_policy(paramiko.AutoAddPolicy()); s.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Restore geo-optimization.php with correct permissions
s.exec_command("cp /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.off /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php", timeout=5)
s.exec_command("chown www-data:www-data /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php", timeout=5)
s.exec_command("php -l /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php 2>&1", timeout=5)

# Flush cache
s.exec_command("cd /www/wwwroot/resource_site && wp cache flush --allow-root 2>&1", timeout=15)
s.exec_command("rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/* 2>/dev/null", timeout=5)

# Verify
stdin,stdout,stderr=s.exec_command("ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php", timeout=5)
print("File: %s" % stdout.read().decode().strip())

s.close()
print("Done!")