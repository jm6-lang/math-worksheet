import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Clear old lock
ssh.exec_command("rm -f /www/wwwroot/resource_site/auto_collect/collector.lock", timeout=5)

# Start in background using nohup
ssh.exec_command(
    "cd /www/wwwroot/resource_site/auto_collect && nohup python3 collector.py >> logs/run_20260407.log 2>&1 & disown",
    timeout=5
)
print("采集已后台启动")
ssh.close()

# Wait
print("等待采集完成(50秒)...")
time.sleep(50)

# Check result
ssh2 = paramiko.SSHClient()
ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh2.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)
stdin, stdout, stderr = ssh2.exec_command(
    "tail -60 /www/wwwroot/resource_site/auto_collect/logs/run_20260407.log",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace')
print(out)
ssh2.close()
