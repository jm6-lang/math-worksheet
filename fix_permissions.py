import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Fix permissions!
print("Fixing file ownership...")
cmd = "chown www-data:www-data /www/wwwroot/resource_site/wp-config.php && chmod 640 /www/wwwroot/resource_site/wp-config.php && echo fixed"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("wp-config: %s" % stdout.read().decode().strip())

# Fix all files we modified
files = [
    "/www/wwwroot/resource_site/robots.txt",
    "/www/wwwroot/resource_site/.well-known/ai-plugin.json",
    "/www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php.off",
    "/www/wwwroot/resource_site/wp-content/mu-plugins-disabled/geo-optimization.php.off",
    "/www/wwwroot/resource_site/wp-content/mu-plugins-disabled/.keep.php",
]
for f in files:
    ssh.exec_command("chown www-data:www-data %s 2>/dev/null" % f, timeout=5)

# Fix mu-plugins dir content
ssh.exec_command("chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/mu-plugins* 2>/dev/null", timeout=5)
ssh.exec_command("chown -R www-data:www-data /www/wwwroot/resource_site/.well-known 2>/dev/null", timeout=5)

# Also fix the GEO mu-plugin if we re-enable it
# First restore it with correct ownership
ssh.exec_command("cp /www/wwwroot/resource_site/wp-content/mu-plugins-disabled/geo-optimization.php.off /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php 2>/dev/null", timeout=5)
ssh.exec_command("chown www-data:www-data /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php && echo 'geo plugin fixed'", timeout=5)

# Re-enable all plugins via wp-cli
import time
time.sleep(1)

# Activate rank-math back (it was active before)
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp plugin activate seo-by-rank-math autoptimize elementor featured-image-from-url internal-links webp-express wp-sweep --allow-root 2>&1",
    timeout=30
)
print("Plugins: %s" % stdout.read().decode('utf-8', errors='ignore')[:500])

# Test
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null", timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()
