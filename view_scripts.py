import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check collector.py
stdin, stdout, stderr = ssh.exec_command(
    "head -100 /www/wwwroot/resource_site/auto_collect/collector.py",
    timeout=10
)
print("=== collector.py (first 100 lines) ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check crawler.py
stdin, stdout, stderr = ssh.exec_command(
    "head -50 /www/wwwroot/resource_site/crawler.py",
    timeout=10
)
print("\n=== crawler.py (first 50 lines) ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check cron_collect.sh
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/cron_collect.sh",
    timeout=10
)
print("\n=== cron_collect.sh ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()