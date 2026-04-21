import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22222, username='root', password='Langlang0.', timeout=15)

# Check the last part of the file for proper closure
stdin, stdout, stderr = ssh.exec_command('tail -5 /www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css', timeout=10)
print('=== tail ===')
print(stdout.read().decode('utf-8', errors='replace'))

# Check brace balance
stdin, stdout, stderr = ssh.exec_command("python3 -c \"
css = open('/www/wwwroot/resource_site/wp-content/themes/yymarket/static/css/custom.css').read()
opens = css.count('{')
closes = css.count('}')
print(f'Braces: {opens} open, {closes} close -> {\\\"OK\\\" if opens==closes else \\\"MISMATCH!\\\"}')
\"", timeout=10)
print('=== brace check ===')
print(stdout.read().decode('utf-8', errors='replace'))
err = stderr.read().decode('utf-8', errors='replace')
if err: print(f'STDERR: {err[:300]}')

# Verify the site is still working
stdin, stdout, stderr = ssh.exec_command('curl -s -o /dev/null -w "%{http_code}" https://www.skillxm.cn/', timeout=15)
code = stdout.read().decode().strip()
print(f'Site HTTP status: {code}')

ssh.close()
