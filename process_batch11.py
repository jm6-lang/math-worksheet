#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第十一批（百度网盘带提取码）"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「12个月从0赚到100万美金」链接：https://pan.baidu.com/s/1irl6ngoJPEeMjoCQrBEkgA 提取码：24d2
「百万富翁快车道」链接：https://pan.baidu.com/s/1JAHYYJ2z0TVAXxeWPWaEUA 提取码：mc8r
「炒股养家传记新版」链接：https://pan.baidu.com/s/13uAyoPifs2vI-BHL5L7O5g 提取码：4397
「Solidworks新手练习教程」链接：https://pan.baidu.com/s/1QPPwZ87Vd7XJcoAAtY32YA 提取码：n77n
「PPT简历模板免费下载」链接：https://pan.baidu.com/s/18uSBrfYeRJLAqjncYlUUYw 提取码：1234
「超级个体普通人创造财富的无限游戏」链接：https://pan.baidu.com/s/1qf3PRuEd8B7lNUprOztwyQ 提取码：1234
「新手入行互联网月入6000完全指南」链接：https://pan.baidu.com/s/1BWa_zHOAlDH2695UZbIPgg 提取码：1234
「中医笔记」链接：https://pan.baidu.com/s/1fRk2ImfY3W-E7akzWkFYxQ 提取码：1234
「变频空调维修技术资料格力美的原理与图纸视频教程主板电路图」链接：https://pan.baidu.com/s/13fn_zLJgSkcV6phBeZA9Dg 提取码：1234
「小家电维修从入门到精通」链接：https://pan.baidu.com/s/1PfhiIBk1jfbSh2L6GUjAtw 提取码：1234
「Ai扣子coze自动化工作流教程」链接：https://pan.baidu.com/s/1K6auy23mhGe8Ab2J8St7ag 提取码：1234
「知乎小说项目详细教程」链接：https://pan.baidu.com/s/1H-FtZZtDe9ByonoChH6JzA 提取码：9tk5
「小红书电商项目教程0-1入门全盘玩法解析」链接：https://pan.baidu.com/s/1MW9xHKjxCMVHV94Ghm1lIA 提取码：je38
「爆款电影解说教程一个手机一个电脑就可以做影视解说」链接：https://pan.baidu.com/s/1edQS5ssNBN64NwozUzpN8g 提取码：1234
「闲鱼冷门跑步项目keep代跑有人日入5张」链接：https://pan.baidu.com/s/1nm32PbjqybgSh-fEb4Mguw 提取码：1234
「爆款自媒体起号训练营14天落地实操训练营」链接：https://pan.baidu.com/s/1Q_6UUhM8qG8Iud7DYY9svQ 提取码：1234
「Ai图文带货实操课新手从0-1实操课」链接：https://pan.baidu.com/s/1vtmiXvBWCq9B37ckyZApUg 提取码：1234
「小红书店铺课程」链接：https://pan.baidu.com/s/1qTRWL99KKV1OPYIELsdNWQ 提取码：1234
「微头条公众号小绿书精准引流男粉到私域卖套图无脑操作有手就行每单99-200每天5单」链接：https://pan.baidu.com/s/1tsyTteNPY37fgOL53MzE6w 提取码：1234
「电影窒恋4k」链接：https://pan.baidu.com/s/1w_0I2QynscpT843Et7aQtw 提取码：1234
「小说资源合集」链接：https://pan.baidu.com/s/1udMbrWZPYH-797id14cK6w 提取码：1234
"""

entries = []
for line in raw_data.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
    # 匹配标题、链接和提取码
    m = re.match(r'[「『【]?(.*?)[」』】]?\s*(?:，|。)?\s*(?:链接[：:]?)?\s*(https?://[^\s]+)\s*(?:提取码[：:]?)?\s*(\w+)?', line)
    if m:
        title = m.group(1).strip()
        title = re.sub(r'^[「『【]+|[」』】]+$', '', title).strip()
        url = m.group(2).strip()
        code = m.group(3).strip() if m.group(3) else ''
        if title and url:
            entries.append({'title': title, 'url': url, 'code': code})

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
    link_code = entry.get('code', '')
    
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
            # 百度网盘显示提取码
            if link_code:
                link_html = '\\n\\n<h3>📥 资源下载</h3>\\n<p>网盘链接：<a href="{}" target="_blank" rel="noopener">{}</a></p>\\n<p>提取码：{}</p>'.format(link_url, link_url, link_code)
            else:
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
