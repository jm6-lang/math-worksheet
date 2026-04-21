import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Install Yoast SEO
    "wp plugin install wordpress-seo --activate --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Re-activate xenice-seo too (don't break anything)
    "wp plugin activate xenice-seo --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Set site title/description for SEO
    "wp option update blogname 'AI知识资源网' --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    "wp option update blogdescription '汇集AI教程、设计软件、影视资源、跨境电商、自媒体运营等高质量免费学习资源，每日更新。' --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Configure Yoast basic
    "wp option update yoast_enable_xml_sitemap 1 --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Flush rewrite rules
    "wp rewrite flush --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
    
    # Clear cache
    "rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/* 2>/dev/null && echo 'cache-cleared'",
    "wp cache flush --allow-root --path=/www/wwwroot/resource_site/ 2>&1",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=60)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    if err: print("ERR: " + err, flush=True)
    print(flush=True)

import time
time.sleep(2)

# Test sitemap
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/sitemap_index.xml' 2>/dev/null | head -15")
print("Sitemap:\n" + stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

# Test footer
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=6' 2>/dev/null | grep -c 'sitemap'")
print("Footer sitemap count: " + stdout.read().decode().strip(), flush=True)

ssh.close()
