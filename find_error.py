import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Find all functions.php files in theme
    "find /www/wwwroot/resource_site/wp-content/themes/yymarket/ -name 'functions*.php' -exec wc -l {} \\;",
    
    # Check if theme has inc/ directory
    "find /www/wwwroot/resource_site/wp-content/themes/yymarket/ -name '*.php' -exec wc -l {} \\; | sort -rn | head -10",
    
    # Check theme directory structure
    "find /www/wwwroot/resource_site/wp-content/themes/yymarket/ -type f -name '*.php' | head -20",
    
    # The error comes from xenice-seo plugin, not theme - check that
    "find /www/wwwroot/resource_site/wp-content/plugins/xenice-seo/ -name '*.php' -exec wc -l {} \\; | sort -rn | head -5",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    print(flush=True)

ssh.close()
