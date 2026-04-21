# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

commands = [
    # 1. Check current SEO plugins
    "wp plugin list --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null | grep -i 'seo\\|rank\\|yoast\\|sitemap\\|all-in-one'",
    
    # 2. Check current theme
    "wp theme list --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null",
    
    # 3. Check permalink structure
    "wp option get permalink_structure --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null",
    
    # 4. Check current robots.txt
    "cat /www/wwwroot/skillxm.cn/public/robots.txt 2>/dev/null || echo 'No robots.txt'",
    
    # 5. Check if sitemap exists
    "ls -la /www/wwwroot/skillxm.cn/public/sitemap* 2>/dev/null || echo 'No sitemap'",
    
    # 6. Check wp-config for important settings
    "grep -E 'WP_DEBUG|DISALLOW_FILE_EDIT|WP_POST_REVISIONS' /www/wwwroot/skillxm.cn/public/wp-config.php 2>/dev/null",
    
    # 7. Count posts by category for tag planning
    "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT t.name, COUNT(*) FROM wp_term_relationships r JOIN wp_term_taxonomy tt ON r.term_taxonomy_id=tt.term_taxonomy_id JOIN wp_terms t ON tt.term_id=t.term_id WHERE tt.taxonomy='category' GROUP BY t.name ORDER BY COUNT(*) DESC;\"",
    
    # 8. Check existing tags
    "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_terms t JOIN wp_term_taxonomy tt ON t.term_id=tt.term_id WHERE tt.taxonomy='post_tag';\"",
    
    # 9. Check if posts have meta descriptions (yoast/rankmath meta)
    "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key LIKE '%_description%' OR meta_key LIKE '%meta_description%';\"",
    
    # 10. Check site title and description
    "wp option get blogname --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null",
    "wp option get blogdescription --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null",
]

for cmd in commands:
    print("=" * 60, flush=True)
    print(cmd, flush=True)
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    if err and 'Warning' not in err:
        print("ERR: {}".format(err[:200]), flush=True)
    print(flush=True)

ssh.close()
