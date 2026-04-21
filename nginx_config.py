import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Full nginx config
cmd = "cat /etc/nginx/sites-enabled/resource_site.conf 2>/dev/null || cat /etc/nginx/sites-available/resource_site.conf 2>/dev/null || cat /etc/nginx/conf.d/resource_site.conf 2>/dev/null || echo 'NOT FOUND'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Nginx config:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
