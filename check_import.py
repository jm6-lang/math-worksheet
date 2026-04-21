import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check progress
stdin, stdout, stderr = ssh.exec_command("cat /tmp/image_import.log 2>/dev/null")
log_content = stdout.read().decode()
print("=== IMPORT LOG ===")
print(log_content)

# Check if still running
stdin, stdout, stderr = ssh.exec_command("ps aux | grep full_import | grep -v grep")
if stdout.read().decode().strip():
    print("\n[Status] Process is still running")
else:
    print("\n[Status] Process completed")

ssh.close()