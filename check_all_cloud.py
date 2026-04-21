# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

check_script = r'''# -*- coding: utf-8 -*-
import pymysql

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Check how many posts have cloud info vs don't
cursor.execute("SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish'")
total = cursor.fetchone()[0]
print("Total published posts: {}".format(total))

cursor.execute("SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish' AND (post_content LIKE '%迅雷%' OR post_content LIKE '%网盘名称%' OR post_content LIKE '%百度网盘%' OR post_content LIKE '%阿里云盘%' OR post_content LIKE '%夸克网盘%')")
has_info = cursor.fetchone()[0]
print("Have cloud info: {}".format(has_info))

cursor.execute("SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_content NOT LIKE '%迅雷%' AND post_content NOT LIKE '%网盘名称%' AND post_content NOT LIKE '%百度网盘%' AND post_content NOT LIKE '%阿里云盘%' AND post_content NOT LIKE '%夸克网盘%' AND post_content NOT LIKE '%网盘来源%'")
missing_info = cursor.fetchone()[0]
print("Missing cloud info: {}".format(missing_info))

# Check which cloud platforms are in the links
cursor.execute("SELECT post_content FROM wp_posts WHERE post_type='post' AND post_status='publish' LIMIT 5")
for row in cursor.fetchall():
    content = row[0]
    # Find all links
    import re
    links = re.findall(r'https?://[^\s<>"\']+', content)
    for link in links:
        if 'xunlei' in link:
            print("Link domain: 迅雷网盘 - {}".format(link[:60]))
            break
        elif 'pan.baidu' in link:
            print("Link domain: 百度网盘 - {}".format(link[:60]))
            break
        elif 'aliyundrive' in link:
            print("Link domain: 阿里云盘 - {}".format(link[:60]))
            break
        elif 'quark' in link:
            print("Link domain: 夸克网盘 - {}".format(link[:60]))
            break
        else:
            print("Link domain: 其他 - {}".format(link[:60]))
            break

conn.close()
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/check_cloud.py', 'w') as f:
    f.write(check_script)
sftp.close()

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 check_cloud.py", timeout=60)
output = stdout.read().decode('utf-8', errors='replace')
print(output, flush=True)

ssh.close()
