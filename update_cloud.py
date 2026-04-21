# -*- coding: utf-8 -*-
# Update recent posts to add cloud storage platform name
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

update_script = r'''# -*- coding: utf-8 -*-
import pymysql
import time
import hashlib

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Get posts from the recent batch (ID 715 onwards, skip 711-714 which are different content)
cursor.execute("SELECT ID, post_title, post_content FROM wp_posts WHERE post_type='post' AND post_status='publish' AND ID >= 715 AND ID <= 736 ORDER BY ID")
rows = cursor.fetchall()

print("Found {} posts to update".format(len(rows)), flush=True)

for post_id, title, content in rows:
    # Check if already has cloud platform info
    if "网盘名称" in content or "迅雷" in content:
        print("[SKIP] ID:{} - already has cloud info".format(post_id), flush=True)
        continue
    
    # Add cloud platform info after the resource type line
    # Find the position after "资源类型：..."
    if "资源类型：" in content:
        new_content = content.replace(
            "资源类型：",
            "资源类型：迅雷网盘\n<p>网盘来源：迅雷云盘（点击链接直接跳转，无需保存到网盘）</p>\n<p>"
        )
    else:
        new_content = content
    
    # Add download note
    if "温馨提示" not in new_content:
        new_content = new_content.replace(
            "</p>",
            "<p>⭐ <strong>使用方法：</strong>复制链接 → 打开迅雷APP → 自动识别并打开资源 → 保存到自己的网盘即可使用</p></p>",
            1
        )
    
    try:
        cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (new_content, post_id))
        conn.commit()
        print("[OK] ID:{} updated".format(post_id), flush=True)
    except Exception as e:
        conn.rollback()
        print("[FAIL] ID:{} - {}".format(post_id, e), flush=True)

conn.close()
print("\nDone!", flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/update_cloud_info.py', 'w') as f:
    f.write(update_script)
sftp.close()

print("Updating posts with cloud storage info...", flush=True)

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 update_cloud_info.py", timeout=60)
output = stdout.read().decode('utf-8', errors='replace')
print(output, flush=True)

ssh.close()
