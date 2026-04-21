import paramiko, sys
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = "<p><strong>{}</strong></p><p>{}</p><h3>下载链接：</h3><p><strong>夸克网盘：</strong> <a href=\"{}\">{}</a></p><blockquote><p>提示：复制链接打开夸克APP即可保存。资源来自网络，仅供学习交流。</p></blockquote>".format(desc, desc, link, link) + css
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    c = body.replace("\\", "\\\\").replace("'", "\\'")
    pn = "book-{}-{}".format(int(time.time()), abs(hash(title)) % 10000)
    sql = "INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count) VALUES (1,'{}','{}','{}','{}','','publish','open','open','','{}','','','{}','{}','',0,'',0,'post','',0);".format(now, now, c, t, pn, now, now)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_p.sql', 'w') as f:
        f.write(sql)
    sftp.close()
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_p.sql 2>&1")
    err = stderr.read().decode().strip()
    if err and 'error' in err.lower():
        print("  SQL ERR: {}".format(err[:80]), flush=True)
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

# 补充漏传的资源 - 这些是之前遗漏的
resources = [
    # 第二个德国巴伐利亚图书馆链接（不同分享码）
    ('德国巴伐利亚图书馆中国汉籍藏书728册PDF', '德国巴伐利亚州立图书馆藏中国汉籍，728册PDF共125GB珍贵文献。', 'https://pan.quark.cn/s/df45d59c2b50', 90),
    # 第二个台北故宫博物院链接（不同分享码）
    ('台北故宫博物院甲库善本珍藏100册', '台北故宫博物院甲库善本珍藏100册33GB，宫廷珍藏善本影印资料。', 'https://pan.quark.cn/s/e779885b546b', 90),
]

ok = 0
total = len(resources)
print("Publishing {} missed resources...".format(total), flush=True)

for i, (t, d, l, c) in enumerate(resources):
    print("[{}/{}] {}...".format(i+1, total, t[:25]), flush=True)
    pid = publish(t, d, l, c)
    if pid:
        print("  OK ID:{}".format(pid), flush=True)
        ok += 1
    else:
        print("  FAILED", flush=True)

ssh.close()
print("\nDone: {}/{}".format(ok, total), flush=True)
