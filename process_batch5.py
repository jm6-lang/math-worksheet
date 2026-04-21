#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第五批（迅雷网盘）"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「manus手机版先保存再使用」链接：https://pan.xunlei.com/s/VOOk8y1nkJX_aZwoiNkZHARXA1?pwd=uai3#
「manus邀请码」链接：https://pan.xunlei.com/s/VOOk9I6HqwD7OHSTuQaoRez2A1?pwd=jwv5#
「人工智能AI变现课程」链接：https://pan.xunlei.com/s/VOOuLU3-dxoVSJw1VI9lWiRRA1?pwd=4tu5#
「扣子空间邀请码共享转存后每天更新」链接：https://pan.xunlei.com/s/VOOuNJ8h_mrrD5nVVcfC8WfZA1?pwd=7z3u#
「AI换脸工具视频教程」链接：https://pan.xunlei.com/s/VOQBYU4VXCgrMtHoYtxoDQk8A1?pwd=t5za#
「Autosale智能体」链接：https://pan.xunlei.com/s/VOWmgpCqKF-zqmyiUwZGQtzeA1?pwd=jdp4#
「网红事件盘点2024」链接：https://pan.xunlei.com/s/VOOaLdH0NXCPatYST9wbCSMwA1?pwd=xj4n#
「尽情做吧」链接：https://pan.xunlei.com/s/VOOaMMvf1yz9mkQ2Yu4Gwd5pA1?pwd=p7np#
「香港片100多部3限制」链接：https://pan.xunlei.com/s/VOOk8r3ZNr60xSX58xAkQdCpA1?pwd=8v23#
「崔X圆写真集」链接：https://pan.xunlei.com/s/VOOk9969bGwx5MQQ0QJfb-CpA1?pwd=8zzp#
「R剧无法抗拒的他」链接：https://pan.xunlei.com/s/VOOk9YF7jzyusr1gOGWKw_3fA1?pwd=yes6#
「R剧你继承的香味」链接：https://pan.xunlei.com/s/VOOk9cvlMTfrgvL65SsfAEYZA1?pwd=btpw#
「高分限制J海外剧合集」链接：https://pan.xunlei.com/s/VOOkAJjXW8g7WN27wQOnTIc_A1?pwd=s7ve#
「美图壁纸福利多多」链接：https://pan.xunlei.com/s/VOOkAcqtZFYSkXrXmyA_uzZ3A1?pwd=rz2p#
「五部Cult片」链接：https://pan.xunlei.com/s/VOOuKsUT6h3GU2868l7ZKmFSA1?pwd=xu5h#
「情深非色全球获奖经典QingSe艺术片十部」链接：https://pan.xunlei.com/s/VOOuKwndvJRJ0EepbPeAw7MyA1?pwd=9wba#
「女xy者」链接：https://pan.xunlei.com/s/VOOuL0aAjH4UyhXMAlzWVl82A1?pwd=j4qh#
「晚上偷偷看韩国理论差边剧情」链接：https://pan.xunlei.com/s/VOOuL6b_-E0mdDZCvo3pxM8sA1?pwd=uwux#
「017影视珍藏」链接：https://pan.xunlei.com/s/VOOuLqit6h3GU2868l7ZL8v2A1?pwd=havm#
「T剧不爱爱」链接：https://pan.xunlei.com/s/VOOuM8FY4_-Pa6ix4UC9NJCPA1?pwd=6wkv#
「网红姬解压密码123」链接：https://pan.xunlei.com/s/VOP3sixUKjtMjvAjm26Zf61EA1?pwd=fr6n#
「女销售」链接：https://pan.xunlei.com/s/VOP3syDPNlevTgYvIlxXySjnA1?pwd=6zbe#
「自备纸巾」链接：https://pan.xunlei.com/s/VOP43vvv1uIGNBJn5Z3gMqj6A1?pwd=xy8a#
「收费短剧合集361部」链接：https://pan.xunlei.com/s/VOP447l0eHRZY2IUihc2awLMA1?pwd=nyzc#
「互换」链接：https://pan.xunlei.com/s/VOP44D4GPMbWlfaBLu59XMIiA1?pwd=iqzb#
「女朋友」链接：https://pan.xunlei.com/s/VOP44IiLmpMnVc4_lh11CRYXA1?pwd=auhi#
「han国3级10部」链接：https://pan.xunlei.com/s/VOP44N163WwJwAbr3_ZNTffFA1?pwd=bfc3#
「吃瓜事件」链接：https://pan.xunlei.com/s/VOP44WO5PMbWlfaBLu59XUdpA1?pwd=r778#
「情非得以写真合集羞答答系列」链接：https://pan.xunlei.com/s/VOP44ehwNlevTgYvIlxY3P3pA1?pwd=xs52#
「海外剧合集」链接：https://pan.xunlei.com/s/VOQ6HfG-iQ_8twVbXwFaQ3f0A1?pwd=abep#
「重磅黑料深夜剧情」链接：https://pan.xunlei.com/s/VOQ6Im6PiQm4XX6zAa85YYiiA1?pwd=zqb9#
「美剧惊悚8级剧情全网独一份」链接：https://pan.xunlei.com/s/VOQ6JLBvhmy4r_XKAnK9ICsjA1?pwd=36d8#
「电影院最新电影每日更新」链接：https://pan.xunlei.com/s/VOQ6JgRr2esiP0XWBKwJkeziA1?pwd=peyx#
「死了都要性」链接：https://pan.xunlei.com/s/VOQ6JmI8iQm4XX6zAa85Z3DUA1?pwd=pyhj#
「不露脸系列」链接：https://pan.xunlei.com/s/VOQ6L46CEA2Y8YjpMwYDDG6-A1?pwd=2fyt#
「香蕉公社」链接：https://pan.xunlei.com/s/VOQ6LMiJWgP9dP95bXLWytT_A1?pwd=bxb8#
「土豪定制」链接：https://pan.xunlei.com/s/VOQ6LSQLaY8k8FITC81_goFhA1?pwd=gkp9#
「美女ASMR未删节」链接：https://pan.xunlei.com/s/VOQ6LcnFPV5TjTtqcfU8ajYAA1?pwd=dv8j#
「主播」链接：https://pan.xunlei.com/s/VOQ6Lp_21euLGlFunrRSjMGVA1?pwd=5mxs#
「jessie捷西」链接：https://pan.xunlei.com/s/VOQ6MXWEFzAAE_8JX7AuhezbA1?pwd=8ani#
"""

entries = []
for line in raw_data.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
    # 匹配夸克和迅雷链接
    m = re.match(r'[「『【]?(.*?)[」』】]?\s*(?:，|。)?\s*(?:链接[：:]?)?\s*(https?://[^\s]+)', line)
    if m:
        title = m.group(1).strip()
        title = re.sub(r'^[「『【]+|[」』】]+$', '', title).strip()
        url = m.group(2).strip()
        if title and url:
            entries.append({'title': title, 'url': url})

print(f"解析到 {len(entries)} 条链接")

links_json = json.dumps(entries, ensure_ascii=False)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

sftp = ssh.open_sftp()
with sftp.open('/tmp/links_batch.json', 'w') as f:
    f.write(links_json)
sftp.close()

match_cmd = '''python3 << 'PYEOF'
import pymysql, re, json

with open('/tmp/links_batch.json', 'r') as f:
    links = json.load(f)

conn = pymysql.connect(host='localhost', user='wp_user', password='gMshA29CshK5', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_title != 'Hello world!'")
articles = {row[1].strip(): row[0] for row in cursor.fetchall()}
print(f"数据库共 {len(articles)} 篇文章")

matched = 0
not_matched = []

for entry in links:
    link_title = entry['title'].strip()
    link_url = entry['url']
    
    found_id = None
    
    if link_title in articles:
        found_id = articles[link_title]
    
    if not found_id:
        for art_title, art_id in articles.items():
            if link_title in art_title or art_title in link_title:
                found_id = art_id
                break
    
    if not found_id:
        clean = re.sub(r'[【】「」『』《》\\[\\]()（）\\s\\d\\-、，。！？]+', '', link_title)
        if len(clean) >= 4:
            for art_title, art_id in articles.items():
                art_clean = re.sub(r'[【】「」『』《》\\[\\]()（）\\s\\d\\-、，。！？]+', '', art_title)
                if clean in art_clean or art_clean in clean:
                    found_id = art_id
                    break
    
    if found_id:
        cursor.execute("SELECT post_content FROM wp_posts WHERE ID = %s", (found_id,))
        content = cursor.fetchone()[0]
        
        if link_url not in content:
            link_html = '\\n\\n<h3>📥 资源下载</h3>\\n<p>网盘链接：<a href="{}" target="_blank" rel="noopener">{}</a></p>'.format(link_url, link_url)
            new_content = content + link_html
            cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (new_content, found_id))
            conn.commit()
            print(f"  [OK] ID={found_id} {link_title[:35]}")
            matched += 1
        else:
            print(f"  [SKIP] ID={found_id} 已有链接")
            matched += 1
    else:
        not_matched.append(link_title)

cursor.close()
conn.close()

print(f"\\n匹配成功: {matched}/{len(links)}")
if not_matched:
    print(f"\\n未匹配 ({len(not_matched)} 条):")
    for t in not_matched[:25]:
        print(f"  - {t[:50]}")
PYEOF'''

stdin, stdout, stderr = ssh.exec_command(match_cmd, timeout=60)
print("\n=== 匹配结果 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.exec_command("rm /tmp/links_batch.json")
ssh.close()
print("\n处理完成。继续发下一批吧。")
