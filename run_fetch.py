import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Run the script
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 fetch_post_images.py 2>&1",
    timeout=180
)

# Stream output
import time
start = time.time()
while not stdout.channel.exit_status_ready() and time.time() - start < 180:
    if stdout.channel.recv_ready():
        print(stdout.channel.recv(1024).decode('utf-8', errors='replace'), end='')
    time.sleep(1)

# Get remaining output
remaining = stdout.read().decode('utf-8', errors='replace')
if remaining:
    print(remaining)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("STDERR:", err)

ssh.close()