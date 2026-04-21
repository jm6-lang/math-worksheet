# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Write a check script to the server
check_script = '''# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Get all published titles
cursor.execute("SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 662 AND ID <= 720 ORDER BY ID")
rows = cursor.fetchall()

with open('/root/scripts/published_titles.txt', 'w', encoding='utf-8') as f:
    for post_id, title in rows:
        f.write("{}\\t{}\\n".format(post_id, title))

print("Done. {} posts saved.".format(len(rows)))

conn.close()
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/check_missing.py', 'w') as f:
    f.write(check_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 check_missing.py")
output = stdout.read().decode('utf-8')
print(output, flush=True)

# Download the result file
sftp = ssh.open_sftp()
with sftp.open('/root/scripts/published_titles.txt', 'r') as f:
    content = f.read()
sftp.close()

print(content, flush=True)

ssh.close()
