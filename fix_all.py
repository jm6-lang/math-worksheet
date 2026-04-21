import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Re-enable ALL plugins
print("Re-enabling all plugins...")
plugins = ['seo-by-rank-math', 'autoptimize', 'elementor', 'featured-image-from-url', 
           'internal-links', 'webp-express', 'wp-sweep']
for p in plugins:
    cmd = "cd /www/wwwroot/resource_site && wp plugin activate %s --allow-root 2>&1" % p
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    result = stdout.read().decode().strip()
    if 'activated' in result.lower() or 'success' in result.lower():
        print("  + %s" % p)
    else:
        print("  x %s: %s" % (p, result[:60]))

# Test
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
code = stdout.read().decode().strip()
print("\nSite: %s" % code)

if code != '200':
    # Try removing WP_CACHE
    print("\nTrying to fix wp-config...")
    sftp = ssh.open_sftp()
    with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'r') as f:
        config = f.read().decode('utf-8')
    
    # Comment out WP_CACHE
    config = config.replace("define('WP_CACHE', true);", "// define('WP_CACHE', true);")
    
    with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'w') as f:
        f.write(config)
    sftp.close()
    print("WP_CACHE commented out")
    
    # Remove advanced-cache
    ssh.exec_command("mv /www/wwwroot/resource_site/wp-content/advanced-cache.php /www/wwwroot/resource_site/wp-content/advanced-cache.php.off 2>/dev/null", timeout=5)
    ssh.exec_command("rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null", timeout=5)
    
    import time
    time.sleep(1)
    stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null", timeout=10)
    print("Site now: %s" % stdout.read().decode().strip())

ssh.close()
