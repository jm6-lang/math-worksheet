import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check for theme issues - switch to default theme temporarily
print("Switching to default theme...")
cmd = "cd /www/wwwroot/resource_site && wp theme activate twentytwentyfour --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("Theme: %s" % stdout.read().decode().strip())

# Test
cmd = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()