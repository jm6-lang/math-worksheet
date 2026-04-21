import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

cmds = [
    'find /www/wwwroot/resource_site/wp-content/themes/yymarket -name "*.css" -type f',
    'grep -rl "@media" /www/wwwroot/resource_site/wp-content/themes/yymarket/ --include="*.css" --include="*.php" 2>/dev/null | head -20',
    'wc -l /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css',
]

for cmd in cmds:
    print(f'=== {cmd[:60]} ===')
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    print(stdout.read().decode('utf-8', errors='replace')[:2000])

ssh.close()
