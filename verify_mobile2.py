import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Check brace balance
stdin, stdout, stderr = ssh.exec_command(
    "grep -o '{' /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css | wc -l"
    , timeout=10)
opens = stdout.read().decode().strip()
stdin, stdout, stderr = ssh.exec_command(
    "grep -o '}' /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css | wc -l"
    , timeout=10)
closes = stdout.read().decode().strip()
print(f'Braces: {opens} open, {closes} close -> {"OK" if opens==closes else "MISMATCH!"}')

# Verify site
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" https://www.skillxm.cn/', timeout=15)
code = stdout.read().decode().strip()
print(f'Site HTTP: {code}')

# Tail check
stdin, stdout, stderr = ssh.exec_command('tail -3 /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
print('Tail:')
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
