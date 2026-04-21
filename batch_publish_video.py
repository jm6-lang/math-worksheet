import paramiko
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = "<p><strong>{}</strong></p><h3>资源介绍：</h3><p>{}</p><h3>下载链接：</h3><p><strong>链接：</strong> <a href=\"{}\">{}</a></p><blockquote><p>提示：复制链接打开对应APP即可保存。资源来自网络，仅供学习交流。</p></blockquote>".format(desc, desc, link, link) + css
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    c = body.replace("\\", "\\\\").replace("'", "\\'")
    pn = "video-{}-{}".format(int(time.time()), abs(hash(title)) % 10000)
    sql = "INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count) VALUES (1,'{}','{}','{}','{}','','publish','open','open','','{}','','','{}','{}','',0,'',0,'post','',0);".format(now, now, c, t, pn, now, now)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_p.sql', 'w') as f:
        f.write(sql)
    sftp.close()
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_p.sql 2>&1")
    err = stderr.read().decode().strip()
    if err and 'error' in err.lower():
        print("  SQL ERR: {}".format(err[:60]), flush=True)
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

# 影视娱乐(86) / 影视在线(88)
resources = [
    ('网红事件盘点2024', '2024年网红热门事件大盘点，年度吃瓜合集。', 'https://pan.xunlei.com/s/VOOaLdH0NXCPatYST9wbCSMwA1?pwd=xj4n#', 86),
    ('尽情做吧', '精彩视频内容合集，休闲娱乐必备。', 'https://pan.xunlei.com/s/VOOaMMvf1yz9mkQ2Yu4Gwd5pA1?pwd=p7np#', 86),
    ('香港限制级电影100多部', '香港经典限制级电影合集第三弹，100+部影片。', 'https://pan.xunlei.com/s/VOOk8r3ZNr60xSX58xAkQdCpA1?pwd=8v23#', 86),
    ('崔X圆写真集', '网红写真集锦，颜值担当作品合集。', 'https://pan.xunlei.com/s/VOOk9969bGwx5MQQ0QJfb-CpA1?pwd=8zzp#', 86),
    ('无法抗拒的他R剧', '韩剧无法抗拒的他全集，热门R级别韩剧。', 'https://pan.xunlei.com/s/VOOk9YF7jzyusr1gOGWKw_3fA1?pwd=yes6#', 86),
    ('你继承的香味R剧', '韩剧你继承的香味全集，热门R级剧集。', 'https://pan.xunlei.com/s/VOOk9cvlMTfrgvL65SsfAEYZA1?pwd=btpw#', 86),
    ('高分限制级海外剧合集', '高分评价限制级海外剧集合集，经典R剧推荐。', 'https://pan.xunlei.com/s/VOOkAJjXW8g7WN27wQOnTIc_A1?pwd=s7ve#', 86),
    ('美图壁纸福利多多', '高清美图壁纸资源合集，福利壁纸大放送。', 'https://pan.xunlei.com/s/VOOkAcqtZFYSkXrXmyA_uzZ3A1?pwd=rz2p#', 86),
    ('五部Cult片', '五部经典Cult邪典电影合集， cult片影迷精选。', 'https://pan.xunlei.com/s/VOOuKsUT6h3GU2868l7ZKmFSA1?pwd=xu5h#', 86),
    ('全球获奖艺术片十部', '全球获奖经典情色艺术片十部，文艺电影推荐。', 'https://pan.xunlei.com/s/VOOuKwndvJRJ0EepbPeAw7MyA1?pwd=9wba#', 86),
    ('女xy者', '女性向视频内容合集。', 'https://pan.xunlei.com/s/VOOuL0aAjH4UyhXMAlzWVl82A1?pwd=j4qh#', 86),
    ('韩国理论差边剧情', '韩国理论边缘剧情影片合集，深度影视作品。', 'https://pan.xunlei.com/s/VOOuL6b_-E0mdDZCvo3pxM8sA1?pwd=uwux#', 86),
    ('017影视珍藏', '017影视珍藏版资源合集。', 'https://pan.xunlei.com/s/VOOuLqit6h3GU2868l7ZL8v2A1?pwd=havm#', 86),
    ('不爱爱T剧', '韩剧不爱爱全集，T剧经典作品。', 'https://pan.xunlei.com/s/VOOuM8FY4_-Pa6ix4UC9NJCPA1?pwd=6wkv#', 86),
    ('网红姬解压版', '网红姬系列解压视频，解压密码123。', 'https://pan.xunlei.com/s/VOP3sixUKjtMjvAjm26Zf61EA1?pwd=fr6n#', 86),
    ('女销售视频', '女性向视频内容合集。', 'https://pan.xunlei.com/s/VOP3syDPNlevTgYvIlxXySjnA1?pwd=6zbe#', 86),
    ('自备纸巾', '精彩视频内容合集，建议自备纸巾观看。', 'https://pan.xunlei.com/s/VOP43vvv1uIGNBJn5Z3gMqj6A1?pwd=xy8a#', 86),
    ('收费短剧合集361部', '361部收费短剧合集，热门短剧一次看个够。', 'https://pan.xunlei.com/s/VOP447l0eHRZY2IUihc2awLMA1?pwd=nyzc#', 88),
    ('互换视频', '视频内容合集。', 'https://pan.xunlei.com/s/VOP44D4GPMbWlfaBLu59XMIiA1?pwd=iqzb#', 86),
    ('女朋友系列', '视频内容合集。', 'https://pan.xunlei.com/s/VOP44IiLmpMnVc4_lh11CRYXA1?pwd=auhi#', 86),
    ('韩国3级电影10部', '韩国R级电影10部合集。', 'https://pan.xunlei.com/s/VOP44N163WwJwAbr3_ZNTffFA1?pwd=bfc3#', 86),
    ('吃瓜事件合集', '吃瓜事件合集，年度热门话题盘点。', 'https://pan.xunlei.com/s/VOP44WO5PMbWlfaBLu59XUdpA1?pwd=r778#', 86),
    ('情非得以写真合集', '情非得以羞答答系列写真合集。', 'https://pan.xunlei.com/s/VOP44ehwNlevTgYvIlxY3P3pA1?pwd=xs52#', 86),
    ('海外剧合集', '海外电视剧合集，英美日韩剧全覆盖。', 'https://pan.xunlei.com/s/VOQ6HfG-iQ_8twVbXwFaQ3f0A1?pwd=abep#', 86),
    ('重磅黑料深夜剧情', '重磅黑料深夜剧情合集，吃瓜必备。', 'https://pan.xunlei.com/s/VOQ6Im6PiQm4XX6zAa85YYiiA1?pwd=zqb9#', 86),
    ('美剧惊悚8级剧情', '美剧惊悚8级剧情合集，全网独一份。', 'https://pan.xunlei.com/s/VOQ6JLBvhmy4r_XKAnK9ICsjA1?pwd=36d8#', 86),
    ('电影院最新电影每日更新', '电影院最新电影资源，每日更新。', 'https://pan.xunlei.com/s/VOQ6JgRr2esiP0XWBKwJkeziA1?pwd=peyx#', 88),
    ('死了都要性', '视频内容合集。', 'https://pan.xunlei.com/s/VOQ6JmI8iQm4XX6zAa85Z3DUA1?pwd=pyhj#', 86),
    ('不露脸系列', '不露脸系列视频合集。', 'https://pan.xunlei.com/s/VOQ6L46CEA2Y8YjpMwYDDG6-A1?pwd=2fyt#', 86),
    ('香蕉公社', '视频内容合集。', 'https://pan.xunlei.com/s/VOQ6LMiJWgP9dP95bXLWytT_A1?pwd=bxb8#', 86),
    ('土豪定制', '土豪定制版视频合集。', 'https://pan.xunlei.com/s/VOQ6LSQLaY8k8FITC81_goFhA1?pwd=gkp9#', 86),
    ('美女ASMR未删节', '美女ASMR未删节版合集。', 'https://pan.xunlei.com/s/VOQ6LcnFPV5TjTtqcfU8ajYAA1?pwd=dv8j#', 86),
    ('主播系列', '主播视频合集。', 'https://pan.xunlei.com/s/VOQ6Lp_21euLGlFunrRSjMGVA1?pwd=5mxs#', 86),
    ('jessie捷西视频', 'jessie捷西视频作品合集。', 'https://pan.xunlei.com/s/VOQ6MXWEFzAAE_8JX7AuhezbA1?pwd=8ani#', 86),
    ('粉丝攒劲福利每周上新', '粉丝攒劲福利资源，每周更新。', 'https://pan.xunlei.com/s/VOQBYmLz4u-CygjX9Tcm0WolA1?pwd=q9qu#', 86),
]

ok = 0
total = len(resources)
print("Publishing {} video resources...".format(total), flush=True)

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