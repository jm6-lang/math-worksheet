# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

fix_script = r'''# -*- coding: utf-8 -*-
import pymysql
import re

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Get all posts missing cloud info
cursor.execute("""SELECT ID, post_content FROM wp_posts WHERE post_type='post' AND post_status='publish' 
    AND post_content NOT LIKE '%%网盘来源%%' 
    AND post_content NOT LIKE '%%使用方法%%'
    ORDER BY ID""")
rows = cursor.fetchall()

print("Found {} posts to update".format(len(rows)), flush=True)

def detect_cloud(link):
    if 'xunlei' in link:
        return '迅雷网盘'
    elif 'pan.baidu' in link:
        return '百度网盘'
    elif 'aliyundrive' in link or 'alipan' in link:
        return '阿里云盘'
    elif 'quark' in link:
        return '夸克网盘'
    elif '123pan' in link:
        return '123云盘'
    elif 'lanzou' in link:
        return '蓝奏云'
    elif 'drive.google' in link:
        return 'Google Drive'
    elif 'mega.nz' in link:
        return 'Mega网盘'
    elif 'mediafire' in link:
        return 'MediaFire'
    else:
        return None

def get_usage_tip(cloud_name):
    tips = {
        '迅雷网盘': '复制链接 → 打开迅雷APP → 自动识别并打开资源 → 保存到自己的网盘即可',
        '百度网盘': '复制链接 → 打开百度网盘APP或网页版 → 保存到自己的网盘即可',
        '阿里云盘': '复制链接 → 打开阿里云盘APP或网页版 → 保存即可',
        '夸克网盘': '复制链接 → 打开夸克APP → 自动识别 → 保存到网盘即可',
        '123云盘': '复制链接 → 打开123云盘 → 保存资源即可',
        '蓝奏云': '点击链接直接下载，无需登录',
        'Google Drive': '复制链接 → 打开浏览器 → 登录Google账号 → 保存到自己的Drive',
    }
    return tips.get(cloud_name, '复制链接到浏览器打开即可')

updated = 0
for post_id, content in rows:
    links = re.findall(r'https?://[^\s<>"\']+', content)
    cloud_name = None
    for link in links:
        cloud_name = detect_cloud(link)
        if cloud_name:
            break
    
    if not cloud_name:
        continue
    
    tip = get_usage_tip(cloud_name)
    
    # Add cloud info before the last closing </p> tag
    cloud_info = '<p>📁 网盘来源：{}</p><p>⭐ <strong>使用方法：</strong>{}</p>'.format(cloud_name, tip)
    
    new_content = content.rstrip()
    if new_content.endswith('</p>'):
        new_content = new_content[:-4] + cloud_info + '</p>'
    else:
        new_content = new_content + cloud_info
    
    try:
        cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (new_content, post_id))
        conn.commit()
        updated += 1
        if updated <= 5 or updated % 20 == 0:
            print("[OK] ID:{} - {}".format(post_id, cloud_name), flush=True)
    except Exception as e:
        conn.rollback()
        print("[FAIL] ID:{} - {}".format(post_id, e), flush=True)

conn.close()
print("\nDone! Updated {} posts.".format(updated), flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/fix_cloud_info.py', 'w') as f:
    f.write(fix_script)
sftp.close()

print("Fixing cloud info for all posts...", flush=True)

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 fix_cloud_info.py", timeout=120)
output = stdout.read().decode('utf-8', errors='replace')
print(output, flush=True)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("STDERR:", err[:500], flush=True)

ssh.close()
