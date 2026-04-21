import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check the posts_need_images file
stdin, stdout, stderr = ssh.exec_command("wc -l /tmp/posts_need_images.txt 2>/dev/null && head -5 /tmp/posts_need_images.txt")
result = stdout.read().decode()
print("Posts needing images:")
print(result)

# Check if process is stuck
stdin, stdout, stderr = ssh.exec_command("ps aux | grep -E 'full_import|wp post|wp media' | grep -v grep")
print("\nRunning processes:")
print(stdout.read().decode())

# Check last lines of log
stdin, stdout, stderr = ssh.exec_command("tail -20 /tmp/image_import.log")
print("\nLast log lines:")
print(stdout.read().decode())

ssh.close()