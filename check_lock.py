import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check lock file
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/auto_collect/collector.lock 2>&1",
    timeout=10
)
print("Lock文件:", stdout.read().decode('utf-8', errors='replace').strip())

# Check if collector is actually running
stdin, stdout, stderr = ssh.exec_command(
    "ps aux | grep collector | grep -v grep",
    timeout=10
)
print("进程:", stdout.read().decode('utf-8', errors='replace').strip())

# Remove lock and run fresh
stdin, stdout, stderr = ssh.exec_command(
    "rm -f /www/wwwroot/resource_site/auto_collect/collector.lock; echo lock_removed",
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
