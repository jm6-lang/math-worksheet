import paramiko
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = "<p><strong>{}</strong></p><p>{}</p><h3>下载链接：</h3><p><strong>链接：</strong> <a href=\"{}\">{}</a></p><blockquote><p>提示：复制链接打开对应APP即可保存。资源来自网络，仅供学习交流。</p></blockquote>".format(desc, desc, link, link) + css
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    c = body.replace("\\", "\\\\").replace("'", "\\'")
    pn = "ai-{}-{}".format(int(time.time()), abs(hash(title)) % 10000)
    sql = "INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count) VALUES (1,'{}','{}','{}','{}','','publish','open','open','','{}','','','{}','{}','',0,'',0,'post','',0);".format(now, now, c, t, pn, now, now)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_p.sql', 'w') as f:
        f.write(sql)
    sftp.close()
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_p.sql 2>&1")
    err = stderr.read().decode().strip()
    if err and 'error' in err.lower():
        return None
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\"")
    pid = stdout.read().decode().strip()
    cat_sql = "INSERT INTO wp_term_relationships (object_id,term_taxonomy_id,term_order) VALUES ({},{},0); UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id={};".format(pid, cat_id, cat_id)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_c.sql', 'w') as f:
        f.write(cat_sql)
    sftp.close()
    ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_c.sql 2>&1")
    return pid

# AI知识(80)
resources = [
    ('manus手机版 AI Agent', 'manus手机版，AI Agent智能体应用，先保存再使用，支持多种AI任务处理。', 'https://pan.xunlei.com/s/VOOk8y1nkJX_aZwoiNkZHARXA1?pwd=uai3#', 80),
    ('manus邀请码', 'manus AI平台邀请码，复制后打开对应APP查看，使用邀请码注册享受专属福利。', 'https://pan.xunlei.com/s/VOOk9I6HqwD7OHSTuQaoRez2A1?pwd=jwv5#', 80),
    ('人工智能AI变现课程', 'AI人工智能变现课程，教你如何利用AI技术实现副业变现，适合创业者和副业从业者。', 'https://pan.xunlei.com/s/VOOuLU3-dxoVSJw1VI9lWiRRA1?pwd=4tu5#', 80),
    ('扣子空间邀请码共享', '扣子空间(Coze)AI平台邀请码，每日持续更新最新资源，抢先体验AI工作流自动化。', 'https://pan.xunlei.com/s/VOOuNJ8h_mrrD5nVVcfC8WfZA1?pwd=7z3u#', 80),
    ('AI换脸工具视频教程', 'AI换脸工具视频详细教程，手把手教你使用AI进行视频换脸，技术宅必备教程。', 'https://pan.xunlei.com/s/VOQBYU4VXCgrMtHoYtxoDQk8A1?pwd=t5za#', 80),
    ('Autosale智能体', 'Autosale AI智能体工具，自动化销售流程的AI助手，提升销售效率的智能工具。', 'https://pan.xunlei.com/s/VOWmgpCqKF-zqmyiUwZGQtzeA1?pwd=jdp4#', 80),
]

ok = 0
total = len(resources)
print("Publishing {} AI resources...".format(total), flush=True)

for i, (t, d, l, c) in enumerate(resources):
    print("[{}/{}] {}...".format(i+1, total, t[:20]), flush=True)
    pid = publish(t, d, l, c)
    if pid:
        print("  OK ID:{}".format(pid), flush=True)
        ok += 1
    else:
        print("  FAILED", flush=True)

ssh.close()
print("\nDone: {}/{}".format(ok, total), flush=True)
