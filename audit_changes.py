import paramiko, json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# 1. Check site title/description
cmds = [
    f"wp option get blogname --allow-root --path={wp}",
    f"wp option get blogdescription --allow-root --path={wp}",
    # 2. Check Yoast postmeta count
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key LIKE '_yoast_wpseo_meta%' OR meta_key LIKE '_yoast_wpseo_focus%'\"",
    # 3. Tags added by me (check recent tags)
    f"wp term list post_tag --format=csv --fields=term_id,name --allow-root --path={wp} | tail -20",
    # 4. robots.txt content
    f"cat /www/wwwroot/resource_site/robots.txt 2>/dev/null | head -20",
    # 5. Yoast sitemap files
    f"ls /www/wwwroot/resource_site/sitemap_index.xml 2>/dev/null && echo EXISTS || echo GONE",
    f"ls /www/wwwroot/resource_site/wp-sitemap.xml 2>/dev/null && echo EXISTS || echo GONE",
    # 6. Yoast plugin status
    f"wp plugin list --allow-root --path={wp} --format=csv --fields=name,status",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(f">>> {c.split('|')[0].split('--path')[0].strip()[-60:]}")
    print(out[:500])
    print()

ssh.close()
