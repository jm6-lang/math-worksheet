import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 1. Check scripts directory
stdin, stdout, stderr = ssh.exec_command("ls -la /root/scripts/ 2>&1", timeout=10)
print("=== /root/scripts/ ===")
print(stdout.read().decode('utf-8', errors='replace'))

# 2. Check crontab
stdin, stdout, stderr = ssh.exec_command("crontab -l 2>&1", timeout=10)
print("=== Crontab ===")
print(stdout.read().decode('utf-8', errors='replace'))

# 3. Check wp-cron (WordPress scheduled tasks)
stdin, stdout, stderr = ssh.exec_command(
    "wp cron event list --allow-root --path=/www/wwwroot/resource_site --fields=hook,next_run,recurrence --format=table --limit=20",
    timeout=15
)
print("=== WP Cron Events ===")
print(stdout.read().decode('utf-8', errors='replace'))
err = stderr.read().decode('utf-8', errors='replace')
if err.strip():
    print("ERR:", err)

# 4. Find any collector scripts
stdin, stdout, stderr = ssh.exec_command(
    "find /root /www -maxdepth 3 \\( -name '*.py' -o -name '*.php' \\) 2>/dev/null | grep -v woocommerce | grep -v elementor | head -30",
    timeout=10
)
print("=== Scripts ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
