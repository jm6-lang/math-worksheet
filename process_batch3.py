#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第三批"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「各种酿酒教程合集」链接：https://pan.quark.cn/s/73e248320385
「八十种各种快餐类美食做法技术大全」链接：https://pan.quark.cn/s/416411e8cb11
「笔记本电脑维修完全手册」链接：https://pan.quark.cn/s/0b28a167e109
「美食实体店配方合集」链接：https://pan.quark.cn/s/5b7444819477
「99套小吃配方+创业落地指南」链接：https://pan.quark.cn/s/1866e2ec8103
「美食实体店配方专题价值上万」链接：https://pan.quark.cn/s/e8d828090e8f
「30多套小吃技术全套视频教程合集」链接：https://pan.quark.cn/s/2153af3ea584
「手办制作视频教程」链接：https://pan.quark.cn/s/f26e42bd23ca
「超详细生存指南」链接：https://pan.quark.cn/s/e82d53c5a7ef
「编绳手工坊编绳基础结法」链接：https://pan.quark.cn/s/aba89bae4edb
「零基础钩针教程视频+PDF教程」链接：https://pan.quark.cn/s/bfd2acf4b881
「麻将学技术训练与技巧完结」链接：https://pan.quark.cn/s/de4f133a1549
「厨师长教你做菜系列合集【71GB】」链接：https://pan.quark.cn/s/8363225a0eed
「精品凉拌菜系列热卤系列课程」链接：https://pan.quark.cn/s/e91162128386
「饭店常点的35套菜详细视频教学」链接：https://pan.quark.cn/s/83a2aface3a4
「招牌菜36套教学视频人人变大厨」链接：https://pan.quark.cn/s/c5cf90a62b23
「摄影超全付费课程合集335GB」链接：https://pan.quark.cn/s/d24f483a8390
「创业资料价值几万的小吃美食教程522道美食」链接：https://pan.quark.cn/s/2cc0a730c8d4
「国宴大师教做菜120道菜合集」链接：https://pan.quark.cn/s/d9177079608f
「普通人翻身逆袭指南50讲秘方建立认知和赚钱的完整体系资料」链接：https://pan.quark.cn/s/9a4c600af5de
「花束花艺教程」链接：https://pan.quark.cn/s/f03e2660a537
「汽车新能源汽车三电实战维修106节」链接：https://pan.quark.cn/s/c4c14e2d4eed
「民谣吉他课程入门+进阶139集」链接：https://pan.quark.cn/s/d2d214209334
「小白一学就会的短视频剪辑课」链接：https://pan.quark.cn/s/bc481341f362
「制作超有爱迷你宠物玩法1张图涨粉1W多元化变现手把手交给你」链接：https://pan.quark.cn/s/34e5cfb0c69c
「职场办公技能总教程」链接：https://pan.quark.cn/s/329d2145d56d
「PS教程初、中、高1」链接：https://pan.quark.cn/s/8db083799b67
「用搜索提升收入掌握最热门的职场技能完结」链接：https://pan.quark.cn/s/a9939f39515f
「龙舌兰放克iPad基础人物插画课程」链接：https://pan.quark.cn/s/e30142534809
「Blender3.0零基础快速入门课程」链接：https://pan.quark.cn/s/84812fc41aac
「office教程和office模板合集」链接：https://pan.quark.cn/s/965b309d3a40
「职场102项技能课程合集」链接：https://pan.quark.cn/s/2d934cc344c9
「沙雕动画制作教学课程针对0基础小白从文案配音到素材到制作详细实战演示」链接：https://pan.quark.cn/s/819283319088
「全网最全付费声乐技巧唱歌技巧乐理课程视唱练耳教程合集」链接：https://pan.quark.cn/s/1fcd03215800
「Pr速成3小时学会视频剪辑」链接：https://pan.quark.cn/s/3f552246e46b
「StableDiffusion零基础入门课」链接：https://pan.quark.cn/s/ae7ba4bd1999
「摄影剪辑教程大合集」链接：https://pan.quark.cn/s/e8d651ec735d
「大万万老师PS功能精通课」链接：https://pan.quark.cn/s/df4f8acc5070
「短剧剪辑解说课实操班29节」链接：https://pan.quark.cn/s/eea2c124596b
「谷歌优化师部落GoogleSEO零基础入门系列教程」链接：https://pan.quark.cn/s/afdf5a0a2b2c
「少儿编程scratch3.0全套课程214节」链接：https://pan.quark.cn/s/8969377e00eb
「高分R剧合集」链接：https://pan.quark.cn/s/50d8a466cff8
「神楽坂真冬合集你懂的」链接：https://pan.quark.cn/s/28a5d683ad90
「美女集中营3羞涩短剧电影」链接：https://pan.quark.cn/s/bc1c588b4a71
「025吃瓜合集2024年」链接：https://pan.quark.cn/s/d18fd592cb83
「无耻之徒1-11季高清未删减版」链接：https://pan.quark.cn/s/49ffb153d7ed
「19禁电影合集」链接：https://pan.quark.cn/s/d05533554d40
「各平台汽车直播走光直播视频合集」链接：https://pan.quark.cn/s/646d4600c928
「欧美剧3限制」链接：https://pan.quark.cn/s/9859c6e37805
「欧美大尺度电影60部」链接：https://pan.quark.cn/s/11b2dee2f3ec
「世界十大超高分丧尸电影」链接：https://pan.quark.cn/s/fee99c1cf8d5
「韩国最出色的十一部R限制39.7GB」链接：https://pan.quark.cn/s/bdcc69393882
「儿童动画片合集」链接：https://pan.quark.cn/s/73ce18d63ad1
「懂的都懂系列深夜必看韩国电影40部」链接：https://pan.quark.cn/s/8386290d0b82
「女神们的电影合集」链接：https://pan.quark.cn/s/403f548fb740
「25年短剧合集」链接：https://pan.quark.cn/s/ba980fa4111f
「世界十大超高分丧尸电影123GB」链接：https://pan.quark.cn/s/bf732d4edf3a
「评分最高的恐怖片」链接：https://pan.quark.cn/s/d9e7970df78c
「这辈子必看的灾难电影大片」链接：https://pan.quark.cn/s/bd4befba8051
「韩剧合集」链接：https://pan.quark.cn/s/96401fd08a3d
「七部经典大尺度影视剧合集超清」链接：https://pan.quark.cn/s/5171fb2f66a2
「影视合集更新6月」链接：https://pan.quark.cn/s/5f8d038e64e9
「影视合集更新5月」链接：https://pan.quark.cn/s/e43dca5a0a99
「R-日剧合集」链接：https://pan.quark.cn/s/d7a74a75e8ab
「T-泰剧合集」链接：https://pan.quark.cn/s/0566f6e392e6
「O-欧美剧」链接：https://pan.quark.cn/s/7ad55b2f0d36
「全球记录片合集」链接：https://pan.quark.cn/s/1ff111c917c2
「全网最全恐怖片合集1.7TB电影」链接：https://pan.quark.cn/s/c3c77ed22f43
「人人影视全站电影合集600部1TB珍藏版」链接：https://pan.quark.cn/s/b5eb2f729110
「豆瓣电影Top250 723GB」链接：https://pan.quark.cn/s/bd494ceae934
「三部限制级惊悚片高血压远离」链接：https://pan.quark.cn/s/671dca4a6b43
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
    for t in not_matched[:20]:
        print(f"  - {t[:50]}")
PYEOF'''

stdin, stdout, stderr = ssh.exec_command(match_cmd, timeout=60)
print("\n=== 匹配结果 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.exec_command("rm /tmp/links_batch.json")
ssh.close()
print("\n处理完成。继续发下一批吧。")
