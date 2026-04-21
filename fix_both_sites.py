import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

import time
time.sleep(2)

cmds = [
    # Check resource_site wp-config
    "grep 'DB_NAME\\|DB_HOST' /www/wwwroot/resource_site/wp-config.php | head -3",
    
    # Check if site works now (after switch back)
    "curl -sk 'https://skillxm.cn/' 2>/dev/null | wc -c",
    "curl -sk 'https://skillxm.cn/' 2>/dev/null | head -c 500",
    
    # Check mu-plugins in resource_site
    "ls /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>/dev/null || echo 'no-mu-plugins'",
    
    # Create mu-plugins in resource_site too
    "mkdir -p /www/wwwroot/resource_site/wp-content/mu-plugins",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    print(flush=True)

# Now we need to add the SEO footer to the ACTIVE site (resource_site)
footer = '''<?php
add_action('wp_footer', function() {
    echo '<div style="text-align:center;padding:20px 0;font-size:13px;color:#999;background:#f5f5f5;border-top:1px solid #eee;">';
    echo '<a href="https://skillxm.cn/sitemap_index.xml" style="color:#666;margin:0 10px;">sitemap</a>';
    echo '<a href="https://skillxm.cn/robots.txt" style="color:#666;margin:0 10px;">robots</a>';
    echo '</div>';
});
add_action('wp_head', function() {
    if (is_singular('post')) {
        echo '<link rel="canonical" href="'.get_permalink().'" />'."\n";
    }
});
'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/wp-content/mu-plugins/seo-footer.php', 'w') as f:
    f.write(footer)
sftp.close()

# Chown
ssh.exec_command("chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/mu-plugins/", timeout=10)

# Flush cache
ssh.exec_command("rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null; echo 'cache-cleared'", timeout=10)
stdin, stdout, stderr = ssh.exec_command("wp cache flush --allow-root --path=/www/wwwroot/resource_site/ 2>&1")
print("Cache flush: " + stdout.read().decode('utf-8', errors='replace').strip())

time.sleep(2)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=4' 2>/dev/null | wc -c")
print("Page size now: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=4' 2>/dev/null | grep -c 'sitemap'")
print("Sitemap refs: " + stdout.read().decode().strip())

ssh.close()
