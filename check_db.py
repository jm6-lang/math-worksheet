import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Both configs use the same DB 'wp_skillxm', but different users
    # Check if both users can access
    "mysql -uwp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_posts WHERE post_status='publish' AND post_type='post'\" 2>/dev/null",
    "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_posts WHERE post_status='publish' AND post_type='post'\" 2>/dev/null",
    
    # Check Yoast in active site
    "wp plugin list --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null | grep -iE 'yoast|seo'",
    
    # Check active theme
    "wp option get template --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null",
    
    # Check if Yoast sitemap works from active site
    "wp option get yoast_enable_xml_sitemap --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null",
    
    # Check siteurl in active site
    "wp option get siteurl --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null",
    "wp option get home --allow-root --path=/www/wwwroot/resource_site/ 2>/dev/null",
    
    # Check our SEO work - meta descriptions in the DB
    "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key='_yoast_wpseo_metadesc'\" 2>/dev/null",
    
    # Check if our mu-plugin is loading
    "cat /www/wwwroot/resource_site/wp-content/mu-plugins/seo-footer.php | head -5",
    
    # Fix duplicate WP_DEBUG defines in wp-config
    "grep -n 'WP_DEBUG_LOG\\|WP_DEBUG_DISPLAY' /www/wwwroot/resource_site/wp-config.php",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    print(flush=True)

ssh.close()
