import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Check resource_site for WordPress
    "ls /www/wwwroot/resource_site/wp-config.php 2>/dev/null && echo 'HAS-WP' || echo 'NO-WP'",
    "ls /www/wwwroot/resource_site/index.php 2>/dev/null && head -5 /www/wwwroot/resource_site/index.php",
    
    # Check the wp-config in public - does it point to the right DB?
    "grep 'DB_NAME\\|DB_USER\\|DB_PASSWORD' /www/wwwroot/skillxm.cn/public/wp-config.php | head -5",
    
    # Check if maybe resource_site is a symlink
    "ls -la /www/wwwroot/ | grep resource",
    "readlink -f /www/wwwroot/resource_site 2>/dev/null",
    
    # Compare file sizes
    "wc -c /www/wwwroot/resource_site/index.php /www/wwwroot/skillxm.cn/public/index.php 2>/dev/null",
    
    # Check if the public dir has the right wp-content
    "ls /www/wwwroot/skillxm.cn/public/wp-content/plugins/ 2>/dev/null | head -10",
    
    # Check wp-config for table prefix
    "grep 'table_prefix' /www/wwwroot/skillxm.cn/public/wp-config.php",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    print(flush=True)

ssh.close()
