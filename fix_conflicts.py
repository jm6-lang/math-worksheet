import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# List active plugins
cmd = "cd /www/wwwroot/resource_site && wp plugin list --status=active --format=table --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("Active plugins:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

# Deactivate Rank Math (keep Yoast as primary SEO)
print("\nDeactivating rank-math (conflicts with Yoast)...")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp plugin deactivate seo-by-rank-math --allow-root 2>&1",
    timeout=15
)
print("%s" % stdout.read().decode().strip())

# Also deactivate xenice-member which had issues before
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp plugin list --status=active --field=name --allow-root 2>&1 | grep -i xenice",
    timeout=10
)
xenice = stdout.read().decode().strip()
if xenice:
    stdin, stdout, stderr = ssh.exec_command(
        "cd /www/wwwroot/resource_site && wp plugin deactivate %s --allow-root 2>&1" % xenice.strip(),
        timeout=15
    )
    print("Deactivated: %s" % xenice.strip())

import time
time.sleep(2)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/ 2>/dev/null", timeout=10)
print("Site: %s" % stdout.read().decode().strip())

ssh.close()
