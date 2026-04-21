import paramiko, sys
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = f"<p><strong>{desc}</strong></p><h3>资源内容包括：</h3><ul><li>高清完整版资源</li><li>多格式/多清晰度可选</li></ul><h3>下载链接：</h3><p><strong>夸克网盘：</strong> <a href=\"{link}\">{link}</a></p><blockquote><p>提示：复制链接打开夸克APP即可保存</p></blockquote>" + css
    
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    c = body.replace("\\", "\\\\").replace("'", "\\'")
    pn = f"res-{int(time.time())}-{hash(title) % 10000}"
    
    sql = f"INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count) VALUES (1,'{now}','{now}','{c}','{t}','','publish','open','open','','{pn}','','','{now}','{now}','',0,'',0,'post','',0);"
    
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
    
    cat_sql = f"INSERT INTO wp_term_relationships (object_id,term_taxonomy_id,term_order) VALUES ({pid},{cat_id},0); UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id={cat_id};"
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_c.sql', 'w') as f:
        f.write(cat_sql)
    sftp.close()
    ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_c.sql 2>&1")
    return pid

resources = [
    # 书籍资料(81)
    {'t': '小说合集1', 'd': '精选热门小说合集第一弹，海量精品小说一次收齐。', 'l': 'https://pan.quark.cn/s/4011f86fae7f', 'c': 81},
    {'t': '小说合集2', 'd': '精选热门小说合集第二弹，更多好书不容错过。', 'l': 'https://pan.quark.cn/s/62acf4a6f4aa', 'c': 81},
    {'t': '上万本小说合集3', 'd': '上万本小说超大合集，网文实体书全收录。', 'l': 'https://pan.quark.cn/s/46969ebc99ea', 'c': 81},
    {'t': '民间故事合集素材', 'd': '民间故事素材合集，适合创作参考和学习使用。', 'l': 'https://pan.quark.cn/s/2c9e92fdcfdc', 'c': 81},
    {'t': '无限流小说102部合集', 'd': '102部无限流题材小说合集，无限流爱好者必备。', 'l': 'https://pan.quark.cn/s/cc15779bc56c', 'c': 81},
    # 影视娱乐(86)
    {'t': '漫画合集168部304GB', 'd': '168部精选漫画合集，304GB超大容量珍藏版。', 'l': 'https://pan.quark.cn/s/2ecdc523b7b2', 'c': 86},
    {'t': '国漫秦时明月全6季4K', 'd': '国漫巅峰秦时明月全6季，国语中字4K超清。', 'l': 'https://pan.quark.cn/s/a434864fa08e', 'c': 86},
    {'t': '画江湖之不良人1-6季全集', 'd': '画江湖之不良人1-6季完整合集，国漫经典。', 'l': 'https://pan.quark.cn/s/a1eb2634adee', 'c': 86},
    {'t': '约会大作战全系列合集', 'd': '约会大作战S1-S4+赤黑新章前后篇完整合集。', 'l': 'https://pan.quark.cn/s/775379475ef0', 'c': 86},
    {'t': '动漫合集欧美日本', 'd': '欧美日本经典动漫合集，跨区域精选。', 'l': 'https://pan.quark.cn/s/02d6b35340ac', 'c': 86},
    {'t': '日漫电影合集', 'd': '日本动画电影精选合集，口碑佳作全收录。', 'l': 'https://pan.quark.cn/s/a85fe781526f', 'c': 86},
    {'t': '灵珑第二季', 'd': '热门国漫灵珑第二季完整版。', 'l': 'https://pan.quark.cn/s/2994fbf0fe4d', 'c': 86},
    {'t': '宫崎骏电影系列合集', 'd': '宫崎骏吉卜力工作室全部电影作品合集。', 'l': 'https://pan.quark.cn/s/3b76fde794a1', 'c': 86},
    {'t': '爱死机全季合集', 'd': '爱死亡和机器人全季合集，赛博朋克动画神作。', 'l': 'https://pan.quark.cn/s/72efb403ca15', 'c': 86},
    {'t': '漫画屋精选合集', 'd': '漫画屋精选漫画资源合集，海量漫画一次下载。', 'l': 'https://pan.quark.cn/s/aec95a35f1ee', 'c': 86},
    {'t': '动漫合集库', 'd': '动漫资源库大合集，热门番剧经典动漫全覆盖。', 'l': 'https://pan.quark.cn/s/29af05b1591e', 'c': 86},
]

ok = 0
for i, r in enumerate(resources):
    print(f"[{i+1}/16] {r['t'][:20]}...", flush=True)
    pid = publish(r['t'], r['d'], r['l'], r['c'])
    if pid:
        print(f"  OK ID:{pid}", flush=True)
        ok += 1
    else:
        print(f"  FAILED", flush=True)

ssh.close()
print(f"\nDone: {ok}/16", flush=True)
