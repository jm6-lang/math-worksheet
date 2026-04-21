#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第八批（UC网盘）"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「高品质车载DJ音乐大碟」链接：https://drive.uc.cn/s/6b6622c1d37d4?public=1
「精选音乐Mp3合集」链接：https://drive.uc.cn/s/15e7b0d47d884
「Html5+Css3由浅入深教程」链接：https://drive.uc.cn/s/4b1848d6e36b4
「黑帽SEO全套课程」链接：https://drive.uc.cn/s/a5a5518113484
「6天掌握mysql基础视频教程」链接：https://drive.uc.cn/s/4d9b7c9b416a4
「最新C#零基础入门全集」链接：https://drive.uc.cn/s/545c4bad670b4
「JavaWeb新版1」链接：https://drive.uc.cn/s/04fd9d90bf654
「Web前端全栈HTML5+大神之路」链接：https://drive.uc.cn/s/2f1e49b28a674
「正则表达式入门」链接：https://drive.uc.cn/s/e5179da8a5d74
「FCPX全套资源」链接：https://drive.uc.cn/s/383419a0c2694
「记忆大师之李威教程打造最强记忆」链接：https://drive.uc.cn/s/f9e96afb1f7f4
「PS 100款简易字体特效制作教程+源文件+字体」链接：https://drive.uc.cn/s/1208958b6fd94
「C4D渲染器合集」链接：https://drive.uc.cn/s/88809affa5454
「平面设计速成从小白到大神完结」链接：https://drive.uc.cn/s/f33174c45c424
「PS抠图0基础从入门到精通教学秒变大神」链接：https://drive.uc.cn/s/d444f96adca34
「全套高清photoshop网上收费教程」链接：https://drive.uc.cn/s/144eaaa307314
「AI软件系统教程大神带你感受AI的矢量魔法」链接：https://drive.uc.cn/s/1500f5a08f744
「电商合成案例教程大神带你掌握合成技法」链接：https://drive.uc.cn/s/5458d031f4cc4
「某宝买的PS资源」链接：https://drive.uc.cn/s/e0148855f0dd4
「电脑工具合集」链接：https://drive.uc.cn/s/af1d7a0351a54
「JAVA基础到高级全套教程」链接：https://drive.uc.cn/s/3a02d35a08244
「python全套教程」链接：https://drive.uc.cn/s/786079f453dc4
「Dreamweaver CC网页设计从入门到精通」链接：https://drive.uc.cn/s/f7b84e2f7d5a4
「游戏内购合集资源」链接：https://drive.uc.cn/s/7f7b570ae8ef4
「软件合集」链接：https://drive.uc.cn/s/759efdc1128a4
「英语四六级保命班」链接：https://drive.uc.cn/s/0b3f5fbf37c84
「下半年瑞思拜四六级讲义针对12月考试」链接：https://drive.uc.cn/s/b58cb4261b5e4
「小程序开发教程大合集从零基础到精通视频课程」链接：https://drive.uc.cn/s/5e7c7ed278b04
「2025医学类视频课程合集」链接：https://drive.uc.cn/s/fec141e4b2394
「16节实用性爆棚的PS教学走进PhotoshopCC」链接：https://drive.uc.cn/s/781b0df66f524
「淘宝开店教程100节课」链接：https://drive.uc.cn/s/b0f8461696e74
「抖音引流课程日引300粉实战操作方法」链接：https://drive.uc.cn/s/6e0472d6fb964
「哔哩实操运营从0到20万粉已完结」链接：https://drive.uc.cn/s/6c2d2a9040204
「抖音电商抖音小红书电商最新玩法完结」链接：https://drive.uc.cn/s/c553800a1e144
"""

entries = []
for line in raw_data.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
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
