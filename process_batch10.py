#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第十批（百度网盘带提取码）"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「Ai老照片修复懒人包old_photo_restoration」链接：https://pan.baidu.com/s/1OKRcT07QHKdxeCMzlmxCng 提取码：y15h
「AI智能去水印 FliFlik KleanOut for Photo」链接：https://pan.baidu.com/s/1K6rDuhewZwOMGKVFIQctBg 提取码：1c3d
「开源Ai批量抠图工具离线整合包rembg」链接：https://pan.baidu.com/s/1Kk3YqKHxfx5RVZ8eXUZDmw 提取码：yt5o
「小智AI详细教程WIFI版本」链接：https://pan.baidu.com/s/1KWwllYZmMJaXsYFoSWKtpQ 提取码：qwjs
「Topaz Video Enhance AI」链接：https://pan.baidu.com/s/1zJQT_pA1M_xmHsXF8hYENQ 提取码：wn6u
「Luminar Neo AI人工智能修图」链接：https://pan.baidu.com/s/1U7DiqY22VaqudcuhGT0EcQ 提取码：rbeh
「Radiant.Photo AI智能完美照片修图插件」链接：https://pan.baidu.com/s/1Ua8GEAzM6sH_Vg4ilv2l4g 提取码：dtvi
「视频号AI美女最新6.0玩法」链接：https://pan.baidu.com/s/1BoalugDLmEa1EDhaqkvpZA 提取码：1234
「DeepSeek实战手册120集」链接：https://pan.baidu.com/s/1uPlNW-PweWfOFplQCfzg1Q 提取码：1234
「通过DeepSeek变现方式小红书教使用DeepSeek图文导流私域一天变现1000+」链接：https://pan.baidu.com/s/1mc_cPDVtnHeM5AqbCWfo4g 提取码：1234
「DeepSeek玩转公众号流量主日入四位数每天几分钟操作简单零门槛」链接：https://pan.baidu.com/s/1b_wtxHwY6DgUfE3fSg70SA 提取码：1234
「用DeepSeek结合今日头条轻松制作爆款文章单日稳定1000+只需简单复制粘贴即可」链接：https://pan.baidu.com/s/1OyMTW2fOwzysbfQeZfOYHQ 提取码：1234
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
