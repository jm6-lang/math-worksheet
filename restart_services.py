import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Kill all PHP-FPM and Nginx processes
print("Killing old processes...")
ssh.exec_command("killall -9 php-fpm8.1 2>/dev/null; killall -9 nginx 2>/dev/null; echo killed", timeout=10)
import time
time.sleep(2)

# Remove stale socket files
print("Cleaning sockets...")
ssh.exec_command("rm -f /run/php/php8.1-fpm.sock /run/php/php-fpm.sock 2>/dev/null; echo cleaned", timeout=5)
time.sleep(1)

# Start PHP-FPM
print("Starting PHP-FPM...")
stdin, stdout, stderr = ssh.exec_command("systemctl start php8.1-fpm 2>&1", timeout=10)
print("PHP-FPM: %s" % stdout.read().decode().strip())
err = stderr.read().decode().strip()
if err:
    print("  err: %s" % err[:200])

time.sleep(1)

# Start Nginx
print("Starting Nginx...")
stdin, stdout, stderr = ssh.exec_command("systemctl start nginx 2>&1", timeout=10)
print("Nginx: %s" % stdout.read().decode().strip())
err = stderr.read().decode().strip()
if err:
    print("  err: %s" % err[:200])

time.sleep(1)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null", timeout=10)
print("Site: %s" % stdout.read().decode().strip())

# Verify status
stdin, stdout, stderr = ssh.exec_command("systemctl is-active php8.1-fpm nginx 2>/dev/null", timeout=5)
print("Status: %s" % stdout.read().decode().strip())

ssh.close()
