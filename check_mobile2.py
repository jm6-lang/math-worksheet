import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

cmds = [
    # Main CSS - check for @media queries and viewport-related
    'grep -n -i -E "(@media|max-width|min-width|viewport|overflow-x|width.*100|container)" /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/style.css | head -40',
    # Custom CSS content
    'cat /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css',
    # Check header.php for viewport meta tag
    'grep -n "viewport" /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php',
    # Check the main layout containers
    'grep -n -i "container\\|wrapper\\|content-width\\|max-width" /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/style.css | head -20',
]

for cmd in cmds:
    print(f'=== CMD ===')
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    out = stdout.read().decode('utf-8', errors='replace')
    print(out[:3000] if out else '(empty)')
    err = stderr.read().decode('utf-8', errors='replace')
    if err:
        print(f'STDERR: {err[:500]}')

ssh.close()
