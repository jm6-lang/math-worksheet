import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Check the broken line
stdin, stdout, stderr = ssh.exec_command("head -12 /www/wwwroot/resource_site/wp-config.php")
print(stdout.read().decode('utf-8', errors='replace'))

# Fix WPCACHEHOME line - the sed broke the single quotes
stdin, stdout, stderr = ssh.exec_command("sed -i \"10s/.*/define( 'WPCACHEHOME', '\\''\\/www\\/wwwroot\\/resource_site\\/wp-content\\/plugins\\/wp-super-cache\\/'' );/\" /www/wwwroot/resource_site/wp-config.php")

# Verify
stdin, stdout, stderr = ssh.exec_command("sed -n '10p' /www/wwwroot/resource_site/wp-config.php")
line10 = stdout.read().decode('utf-8', errors='replace').strip()
print("Line 10 after fix: " + line10)

ssh.close()
