import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Reload PHP-FPM
stdin, stdout, stderr = ssh.exec_command("kill -USR2 $(cat /run/php/php8.1-fpm.pid 2>/dev/null) 2>&1; echo reload", timeout=10)
print("Reload: %s" % stdout.read().decode().strip() + stderr.read().decode().strip())

# If reload doesn't work, try restart with socket cleanup
ssh.exec_command("rm -f /run/php/php8.1-fpm.sock 2>/dev/null", timeout=5)
stdin, stdout, stderr = ssh.exec_command("systemctl restart php8.1-fpm 2>&1", timeout=15)
print("Restart: %s" % stdout.read().decode().strip() + stderr.read().decode().strip())

import time
time.sleep(3)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -s -D- https://www.skillxm.cn/ 2>/dev/null | head -10", timeout=10)
output = stdout.read().decode('utf-8', errors='ignore')
print("Site:\n%s" % output[:500])

ssh.close()
