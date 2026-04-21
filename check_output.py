import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check what the PHP page actually outputs
cmd = "curl -s https://www.skillxm.cn/ 2>/dev/null | head -50"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("Site output:\n%s" % stdout.read().decode('utf-8', errors='ignore')[:2000])

# Check PHP error
cmd = "curl -s https://www.skillxm.cn/ 2>/dev/null | grep -i 'error\\|fatal\\|warning'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
err = stdout.read().decode('utf-8', errors='ignore')
print("\nErrors:\n%s" % err[:500] if err else "None found in HTML")

ssh.close()
