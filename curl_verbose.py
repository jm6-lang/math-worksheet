import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Full curl output
stdin, stdout, stderr = ssh.exec_command(
    "curl -v https://www.skillxm.cn/ 2>&1",
    timeout=15
)
print(stdout.read().decode('utf-8', errors='ignore')[:3000])

# Also check /var/run/php/
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /var/run/php/ 2>&1",
    timeout=5
)
print("\n/var/run/php/:\n%s" % stdout.read().decode().strip())

ssh.close()
