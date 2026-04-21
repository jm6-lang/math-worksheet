import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Upload
sftp = ssh.open_sftp()
sftp.put(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\server_curl_img.py', 
         '/root/scripts/server_curl_img.py')
sftp.chmod('/root/scripts/server_curl_img.py', 0o755)
sftp.close()
print("Uploaded")

# Run
ssh.exec_command(
    "cd /root/scripts && nohup python3 server_curl_img.py --offset=0 --limit=10 --delay=3 > /root/scripts/add_img_log3.txt 2>&1 &",
    timeout=10
)
print("Started")

ssh.close()