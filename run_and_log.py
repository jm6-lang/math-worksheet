import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check today's log
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/auto_collect/logs/run_20260407.log 2>&1 | tail -30",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("日志:", out if out else "(空)")
print("错误:", err if err else "(无)")

# Run collector and capture output
print("\n运行采集...")
cmd = "cd /www/wwwroot/resource_site/auto_collect && timeout 60 python3 collector.py 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=70)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print("输出:", out[-2000:] if len(out) > 2000 else out)
print("错误:", err[-500:] if len(err) > 500 else err)

ssh.close()
