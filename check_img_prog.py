import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check log
stdin, stdout, stderr = ssh.exec_command(
    "tail -30 /root/scripts/img_log.txt",
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

# Check process
stdin, stdout, stderr = ssh.exec_command(
    "ps aux | grep batch_add_images | grep -v grep",
    timeout=10
)
print("Process:", stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()