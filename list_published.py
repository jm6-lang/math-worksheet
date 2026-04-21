# -*- coding: utf-8 -*-
import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Get all published post titles
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 662 AND ID <= 750;\"")
output = stdout.read().decode('utf-8', errors='ignore')
print("Published posts ID 662-750:", flush=True)
print(output, flush=True)

ssh.close()
