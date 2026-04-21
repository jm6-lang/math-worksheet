# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# ===== Step 1: Activate Yoast SEO and configure =====
commands = [
    # Activate Yoast SEO
    "wp plugin activate wordpress-seo --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
    
    # Set proper site title and description
    "wp option update blogname 'AI知识资源网 - 免费教程/软件/影视/课程资源分享' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
    "wp option update blogdescription '汇集AI教程、设计软件、影视资源、跨境电商、自媒体运营等高质量免费学习资源，每日更新。' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
    
    # Enable XML sitemap in Yoast
    "wp option update yoast_indexable_content_types --format=json '{\"post\":true,\"page\":true,\"attachment\":false}' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1 || echo 'skip1'",
    
    # Set Yoast to show sitemap
    "wp option update yoast_enable_xml_sitemap '1' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1 || echo 'skip2'",
    
    # Enable sitemap via Yoast options
    "wp option update yoast_taxonomy_0_sitemap_include 'always' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1 || echo 'skip3'",
    
    # Disable date archives (duplicate content)
    "wp option update yoast_disable_date_archives '1' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1 || echo 'skip4'",
    
    # Disable author archives
    "wp option update yoast_disable_author_archives '1' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1 || echo 'skip5'",
]

for cmd in commands:
    print(">> {}".format(cmd), flush=True)
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    if err and 'Warning' not in err and 'deprecated' not in err.lower():
        print("ERR: {}".format(err[:200]), flush=True)
    print(flush=True)

# ===== Step 2: Create robots.txt =====
robots_txt = """User-agent: *
Allow: /
Disallow: /wp-admin/
Disallow: /wp-includes/
Disallow: /wp-content/plugins/
Disallow: /wp-content/cache/
Disallow: /trackback/
Disallow: /feed/
Disallow: /comments/
Disallow: /?s=
Disallow: /search/
Disallow: /*?replytocom=
Disallow: /wp-login.php
Disallow: /wp-register.php

Sitemap: https://skillxm.cn/sitemap_index.xml

# Allow main CSS/JS
Allow: /wp-content/themes/
Allow: /wp-content/uploads/
"""

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/skillxm.cn/public/robots.txt', 'w') as f:
    f.write(robots_txt)
print("robots.txt created!", flush=True)

# ===== Step 3: Set Yoast SEO meta for homepage =====
# Set title format and description for homepage
cmds2 = [
    # Yoast social & search appearance settings
    "wp option update yoast_company_name 'AI知识资源网' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
    "wp option update yoast_company_or_person 'company' --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1",
]

for cmd in cmds2:
    print(">> {}".format(cmd), flush=True)
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)

ssh.close()
print("\nStep 1-3 done!", flush=True)
