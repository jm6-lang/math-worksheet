import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Write log to file on local
stdin, stdout, stderr = ssh.exec_command('cat /root/scripts/img_log.txt', timeout=10)
log = stdout.read().decode('utf-8', errors='replace')

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\img_log_output.txt', 'w', encoding='utf-8') as f:
    f.write(log)

ssh.close()
print("Log saved to img_log_output.txt")