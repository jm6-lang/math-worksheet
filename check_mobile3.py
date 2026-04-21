import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Full custom.css
stdin, stdout, stderr = ssh.exec_command('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
print('=== custom.css (FULL) ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Theme style.css mobile section (around max-width:767px)
stdin, stdout, stderr = ssh.exec_command('wc -l /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/style.css', timeout=10)
total_lines = stdout.read().decode().strip()
print(f'\n=== style.css total lines: {total_lines} ===')

# Theme style.css lines 340-380 (near @media max-width:767px for yy-main)
stdin, stdout, stderr = ssh.exec_command('sed -n "340,400p" /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/style.css', timeout=10)
print('\n=== style.css 340-400 ===')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
