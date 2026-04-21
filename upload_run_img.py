import paramiko
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Upload script
script_content = open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\batch_add_images.py', 'rb').read()
sftp = ssh.open_sftp()
sftp.putfo(open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\batch_add_images.py', 'rb'), 
           '/root/scripts/batch_add_images.py')
sftp.chmod('/root/scripts/batch_add_images.py', 0o755)
sftp.close()
print("Uploaded")

# Install requests if missing
ssh.exec_command("pip3 install requests -q", timeout=30)
print("Dependencies installed")

# Run a small batch first
ssh.exec_command(
    "cd /root/scripts && nohup python3 batch_add_images.py --offset=0 --limit=10 --delay=3 > /root/scripts/img_log.txt 2>&1 &",
    timeout=10
)
print("Started batch (10 posts, delay=3s)")

ssh.close()
print("Check progress: tail -f /root/scripts/img_log.txt")
