import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Fix file ownership
    "chown -R www-data:www-data /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/",
    "chmod 644 /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/*.php",
    
    # Check if mu-plugins are loaded
    "wp plugin list --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null | grep -i mu || echo 'no-mu-plugin-column'",
    
    # Check mu-plugins content
    "head -5 /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-footer.php",
    
    # Clear all cache
    "wp cache flush --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
    
    # Check if there's a page cache (LiteSpeed)
    "ls /www/wwwroot/skillxm.cn/public/wp-content/cache/ 2>/dev/null | head -5",
    "rm -rf /www/wwwroot/skillxm.cn/public/wp-content/cache/litespeed/ 2>/dev/null && echo 'litespeed-cache-cleared'",
    
    # Verify PHP syntax
    "php -l /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-footer.php",
    "php -l /www/wwwroot/skillxm.cn/public/wp-content/mu-plugins/seo-jsonld.php",
]

for c in cmds:
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    if err: print("ERR: " + err, flush=True)

# Test again after cache clear
import time
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ 2>/dev/null | grep -c 'sitemap_index'")
print("\nSitemap link count: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/ 2>/dev/null | grep -c '站点地图'")
print("Footer text count: " + stdout.read().decode().strip())

ssh.close()
