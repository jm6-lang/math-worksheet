import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Start collector in background
ssh.exec_command(
    "cd /www/wwwroot/resource_site/auto_collect && nohup python3 collector.py > logs/run_20260407.log 2>&1 &",
    timeout=10
)
print("已后台启动采集脚本")
ssh.close()

# Wait for it to run
import time
time.sleep(50)

# Reconnect and check log
ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

stdin, stdout, stderr = ssh2.exec_command(
    "cat /www/wwwroot/resource_site/auto_collect/logs/run_20260407.log",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace')
# Only print last part
lines = out.split('\n')
print('\n'.join(lines[-40:]))
ssh2.close()
