import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# The ACTIVE site is /www/wwwroot/resource_site, NOT skillxm.cn/public
# All SEO plugins/configs must be in resource_site

# 1. Fix wp-config.php duplicate defines (causes PHP warnings)
stdin, stdout, stderr = ssh.exec_command("head -30 /www/wwwroot/resource_site/wp-config.php")
print("wp-config lines 20-30:", flush=True)
print(stdout.read().decode('utf-8', errors='replace'), flush=True)

# 2. Fix theme functions.php syntax error
stdin, stdout, stderr = ssh.exec_command("sed -n '265,272p' /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php")
print("Theme func lines 265-272:", flush=True)
print(stdout.read().decode('utf-8', errors='replace'), flush=True)

ssh.close()
