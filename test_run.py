import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Try running as www-data (same as cron does)
cmd = "cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector.py 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("=== 输出 ===")
print(out)
if err.strip():
    print("=== 错误 ===")
    print(err)

ssh.close()
