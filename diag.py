import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Check all log files in the logs directory
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/auto_collect/logs/ 2>&1", timeout=10)
print("=== Logs ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check if there's a daily log file for today (Apr 7)
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/logs/run_20260407.log 2>&1", timeout=10)
print("=== Today log (20260407) ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check lock file
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/collector.lock 2>&1", timeout=10)
print("=== Lock file ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check config
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/config.json 2>&1", timeout=10)
print("=== Config ===")
print(stdout.read().decode('utf-8', errors='replace'))

# Check if cron service is running
stdin, stdout, stderr = ssh.exec_command("systemctl status cron 2>&1 | head -10", timeout=10)
print("=== Cron service ===")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()
