import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check progress
stdin, stdout, stderr = ssh.exec_command("cat /tmp/fast_import.log 2>/dev/null")
log = stdout.read().decode()
print("=== IMPORT PROGRESS ===")
print(log)

# Check if running
stdin, stdout, stderr = ssh.exec_command("ps aux | grep fast_import | grep -v grep")
running = stdout.read().decode().strip()
if running:
    print("\n[Status] Still running")
else:
    print("\n[Status] Completed")

# Count media
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp media list --format=count --allow-root 2>/dev/null"
)
media_count = stdout.read().decode().strip()
print(f"\nMedia library count: {media_count}")

ssh.close()