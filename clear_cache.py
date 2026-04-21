import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Remove wp-super-cache files completely
    "rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/",
    "rm -rf /www/wwwroot/resource_site/wp-content/cache/db.php 2>/dev/null",
    
    # Also disable WP_CACHE in wp-config temporarily
    "sed -i \"s/define('WP_CACHE', true)/define('WP_CACHE', false)/\" /www/wwwroot/resource_site/wp-config.php",
    
    # Deactivate wp-super-cache plugin
    "wp plugin deactivate wp-super-cache --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Flush WP cache
    "wp cache flush --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Clear wp-super-cache config
    "wp option delete wp_cache_status --allow-root --path=/www/wwwroot/resource_site/ 2>&1 || echo 'no-option'",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    if err: print("ERR: " + err, flush=True)
    print(flush=True)

import time
time.sleep(2)

# Test again
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?nocache=11' 2>/dev/null | grep -c 'sitemap_index'")
print("Footer link count: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?nocache=11' 2>/dev/null | tail -c 500")
print("Footer area:\n" + stdout.read().decode('utf-8', errors='replace').strip())

# Test JSON-LD on article
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?p=800&nocache=11' 2>/dev/null | grep -c 'ld+json'")
print("JSON-LD: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?p=800&nocache=11' 2>/dev/null | grep 'ld+json' | head -1")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("JSON-LD content: " + (out[:200] if out else "not found"))

ssh.close()
