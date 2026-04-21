import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Check Yoast sitemap index status
    "wp option get yoast_enable_xml_sitemap --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null",
    
    # Try accessing Yoast generated sitemap
    "curl -s https://skillxm.cn/sitemap_index.xml -o /dev/null -w '%{http_code}' 2>/dev/null",
    
    # Check if .htaccess has WordPress rewrite rules (needed for sitemap)
    "cat /www/wwwroot/skillxm.cn/public/.htaccess | grep -i 'wordpress' | head -5 || echo 'no-wp-rewrite'",
    
    # Add WordPress rewrite rules to .htaccess if missing
    "grep -c 'index.php' /www/wwwroot/skillxm.cn/public/.htaccess 2>/dev/null || echo '0'",
    
    # Check LiteSpeed cache plugin
    "wp plugin list --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null | grep -i 'litespeed\\|cache'",
    
    # Verify post-sitemap.xml works
    "curl -s https://skillxm.cn/post-sitemap.xml -o /dev/null -w '%{http_code}' 2>/dev/null",
]
for c in cmds:
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

# Fix: Ensure WordPress rewrite rules are in .htaccess
print("=== Fixing .htaccess ===", flush=True)
stdin, stdout, stderr = ssh.exec_command("wp rewrite flush --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>&1")
print(stdout.read().decode('utf-8', errors='replace'), flush=True)

# Check if WP rewrite rules exist now
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/skillxm.cn/public/.htaccess 2>/dev/null | grep -A3 'RewriteBase' | head -10")
out = stdout.read().decode('utf-8', errors='replace').strip()
print("RewriteBase: {}".format(out), flush=True)

# Verify sitemap again
stdin, stdout, stderr = ssh.exec_command("curl -s https://skillxm.cn/sitemap_index.xml -o /dev/null -w '%{http_code}' 2>/dev/null")
print("Sitemap HTTP status: {}".format(stdout.read().decode().strip()), flush=True)

ssh.close()
