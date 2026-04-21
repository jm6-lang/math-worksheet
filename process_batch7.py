#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第七批"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「中国古玩鉴识知识系列书籍」链接：https://pan.xunlei.com/s/VOOk9ly0JBu9rQyGiwv31UsnA1?pwd=uy8e#
「创业优质教程合集爱看书读好书系列」链接：https://pan.xunlei.com/s/VOOuKbEkRTmQCQcZcBrRvcYtA1?pwd=y96q#
「百病食疗大全彩图精装」链接：https://pan.xunlei.com/s/VOOuKiYOFPUtXUKuIOgMhb4yA1?pwd=nidc#
「用声音修炼气场完结」链接：https://pan.xunlei.com/s/VOOuLYoTRTmQCQcZcBrRvzs-A1?pwd=2xtq#
「梅花易数白话解象数思维的智慧」链接：https://pan.xunlei.com/s/VOOuLe65NaBNlzRDdqMF43NUA1?pwd=kk74#
「富爸爸系列全集纪念新版共32册」链接：https://pan.xunlei.com/s/VOP3rnoD-wEAtCmsdBlggRXRA1?pwd=4m5x#
「书库合集」链接：https://pan.xunlei.com/s/VOQ6I4rzezacrOCmZ3xzNozIA1?pwd=dmnj#
「人人都可以学的顶级思维法套装共7册」链接：https://pan.xunlei.com/s/VOQ6KC01-caw75eeiJRzVHXPA1?pwd=2474#
「富爸爸点石成金富爸爸21世纪的生意富爸爸不公平的优势富爸爸富人的阴谋富爸爸财富大趋势套装共五册」链接：https://pan.xunlei.com/s/VOQ6KI9A7MK-8MadlJlaxMUgA1?pwd=re3g#
「中医补肾壮阳秘方」链接：https://pan.xunlei.com/s/VOQ6MNnRpklQNxGL9FDLjXYdA1?pwd=wqx2#
「父与子的X教尬聊」链接：https://pan.xunlei.com/s/VOQ6Mi03829Ak4YZiGHD5x7yA1?pwd=cy93#
「MBA课程」链接：https://pan.xunlei.com/s/VOQ6MoEjeF5hzjNz8XoKo6nVA1?pwd=mv75#
「中医古籍合集超全系列中医配方正在被鬼子申请专利」链接：https://pan.xunlei.com/s/VOQBckc4OoRRo7e7hTVWQymaA1?pwd=7fqn#
「最新上千套农村自建房图纸合集」链接：https://pan.xunlei.com/s/VOVjp6cmrCI1e6xO09VM77mAA1?pwd=emit#
「解锁版软件找软件请看这里可根据时间排序查找每日更新实用软件请来挑选」链接：https://pan.xunlei.com/s/VOOaMJ54DvaNOzRoOLlxR5o2A1?pwd=a6ub#
「TikTokMod解除限制版」链接：https://pan.xunlei.com/s/VOU7rQiMuAdJSBAnyq_Nm2ZtA1?pwd=ky3z#
「一键迁移网盘资源百度转迅雷」链接：https://pan.xunlei.com/s/VOOaMRjWtx2hjdy5BesUfxSnA1?pwd=cjtj#
「win迅雷最新不限速版」链接：https://pan.xunlei.com/s/VOOaMd0Syh9lX_tN9sdXs7xcA1?pwd=475j#
「wifi万能钥匙SVIP版」链接：https://pan.xunlei.com/s/VOOuLKYI6SticUyS536Y85X2A1?pwd=sdm8#
「UC网盘批量转存工具」链接：https://pan.xunlei.com/s/VOQ6LDS8IEc-3wd4nNsUs6ZpA1?pwd=6ezx#
「夸克网盘批量转存分享工具」链接：https://pan.xunlei.com/s/VOQ6LIBchwbqjdXwYUw4zaeBA1?pwd=n8hd#
「金铲铲单机版超详细的最强教程9999+金币」链接：https://pan.xunlei.com/s/VOQ6Mckoft4N8Zuq13Rr67HKA1?pwd=hvcq#
「骗子酒馆手机版」链接：https://pan.xunlei.com/s/VOQBZq70LnlUbHA45Jg4GXKcA1?pwd=x4sh#
「可灵无限灵感值」链接：https://pan.xunlei.com/s/VOQBZwUyKUAl4DNNfMGcsABPA1?pwd=c2g4#
「全网最全机顶盒视频教程」链接：https://pan.xunlei.com/s/VOQB_yHrz7MdEh5qGBzMq6KiA1?pwd=9fn3#
「迅雷VIP解锁版」链接：https://pan.xunlei.com/s/VOUCp8cC0hTpuOaP6-RwTTTjA1?pwd=psyh#
「微信好友检测工具李跳跳真实好友」链接：https://pan.xunlei.com/s/VOUCs9zzzro06gxXj-OeRpgeA1?pwd=zayh#
「影梭定位修改大师」链接：https://pan.xunlei.com/s/VOUIMuAtd8aW70HVfIb_pG62A1?pwd=5fh6#
「抢福袋工具」链接：https://pan.xunlei.com/s/VOUIqHXWiH86exGXkPLRSPDtA1?pwd=8v5z#
「微粉大师」链接：https://pan.xunlei.com/s/VOUNDvC01nsSdn0t7wIaNlyCA1?pwd=8d5r#
「李跳跳跳广告神器非常好用」链接：https://pan.xunlei.com/s/VOUNExYviH86exGXkPLTs92OA1?pwd=jve7#
「WPS解锁版」链接：https://pan.xunlei.com/s/VOUNGDCYsyKaLN-PfIQOX7_3A1?pwd=2ygu#
「Windows纯净版系统镜像大合集」链接：https://pan.xunlei.com/s/VOVQ1ijdL8qAx5s7vkZ5kTQuA1?pwd=e5c9#
「国外最火应用app合集」链接：https://pan.xunlei.com/s/VOVVM2TMrCI1e6xO09VDc1JuA1?pwd=m4eu#
「电脑系统安装工具包」链接：https://pan.xunlei.com/s/VOVeYGpND22zWV5oqAn7nqJJA1?pwd=4qa9#
「抖音短视频下载提取」链接：https://pan.xunlei.com/s/VOVjsNkfZafTzbx1_YscGDyYA1?pwd=399y#
「去除马赛克」链接：https://pan.xunlei.com/s/VOVp3RqvUtVuXKoLFgchvdgPA1?pwd=6h68#
「AI写作鱼手机号登录终身VIP」链接：https://pan.xunlei.com/s/VOVun5tFShvSW39OHUi_mDjQA1?pwd=vaxg#
「3D动态照片v4.0.0.6解锁版」链接：https://pan.xunlei.com/s/VOVz9TwDFoIhJcrKIoZuY1vHA1?pwd=s489#
「变声器大师破解版」链接：https://pan.xunlei.com/s/VOW3JS-k4-8tmbnwfgZfFBqFA1?pwd=qijb#
「梨园行戏曲TV版v995.7.2解锁会员版资源丰富戏曲爱好者必备」链接：https://pan.xunlei.com/s/VOW8VTmvEiWTwdiuF1dxE9pyA1?pwd=spnp#
「马克全能去水印v1.1.5绿化解锁版抖音快手短视频去水印」链接：https://pan.xunlei.com/s/VOWD_nrQwZcva3xhSMZUf062A1?pwd=j3ed#
「Zapya快牙v6.5.5US解锁版无限制跨平台极速手机文件互传工具」链接：https://pan.xunlei.com/s/VOWIs-iGNCOKKEYQ-SO7zRKZA1?pwd=j5d3#
「作业帮v13.61.0修改解锁绿化免费版高效智能学习辅导APP」链接：https://pan.xunlei.com/s/VOWOBNPwn0pAejN8kN4ulJJ9A1?pwd=vgq4#
「TVBox_takagen99免费版含影视源文件」链接：https://pan.xunlei.com/s/VOWTCi3XrUcu62wAnKAvVD4jA1?pwd=efu4#
「酷我音乐6.0.1.0Mod车机版解锁会员免费听所有音乐」链接：https://pan.xunlei.com/s/VOWYC39PkmCwNNOZD-ixu68QA1?pwd=8nbv#
「Youtube油管视频下载器」链接：https://pan.xunlei.com/s/VOWYEH0EkmCwNNOZD-ixvJFYA1?pwd=jjj2#
「视频去水印神器HitPaw Watermark Remover」链接：https://pan.xunlei.com/s/VOWYHlx03_HvPduhhAQFlYaLA1?pwd=edax#
「轻听音乐v2.2.6免费版无限制多线路免费音乐软件」链接：https://pan.xunlei.com/s/VOWcbhIhc3ogRlnOhWz16z-lA1?pwd=3nbk#
「全球卫星电视TV garden」链接：https://pan.xunlei.com/s/VOWrpwtWTK_RkTvQWYTGJ2pJA1?pwd=s8a8#
「即梦Ai破解版无限积分」链接：https://pan.xunlei.com/s/VOWrq9oLeoQT89x8UX6ZS-cFA1?pwd=h48t#
「动物翻译器」链接：https://pan.xunlei.com/s/VOWrqDLfYa-Iuq5t6PKsOHgYA1?pwd=fi2t#
「搬运工具包」链接：https://pan.xunlei.com/s/VOX6JDhMOOp5Lb8QDfV7mxp4A1?pwd=cx78#
「电脑密码破解工具」链接：https://pan.xunlei.com/s/VOXBRniSZWYhuK2DRAmIJ3HLA1?pwd=gy5h#
「手机版闲鱼助手自动发货」链接：https://pan.xunlei.com/s/VOXGks0nYB0jDG4ROtTuoiJ0A1?pwd=edim#
「图片批量处理」链接：https://pan.xunlei.com/s/VOXW6jHtze9Rl3yZAc9OfK0tA1?pwd=6qcd#
「文件批量重命名」链接：https://pan.xunlei.com/s/VOXW6r92yNaOLWrUcv2qljKzA1?pwd=7hza#
「手机刷机工具箱」链接：https://pan.xunlei.com/s/VOXaFh7CRwAxaJVLO94ZJrKiA1?pwd=ppf6#
「CDR2023中文破解版CorelDRAW」链接：https://pan.xunlei.com/s/VOXfSJnKcx4UdHEqZS9f5viOA1?pwd=2z4i#
「打卡软件神器」链接：https://pan.xunlei.com/s/VOXumZU5y-6A2bPiWO5dRzkrA1?pwd=88aq#
「查企业查信息限制注册即送5年SVIP」链接：https://pan.xunlei.com/s/VOY--vv8UsLDxjyOGMSyLOd5A1?pwd=48gy#
「笔趣阁完美修改去广告解锁高级版随时随地免费畅看」链接：https://pan.xunlei.com/s/VOY42lVZqub9V_5XZd13WCacA1?pwd=g4yv#
「公众号爆文机器人」链接：https://pan.xunlei.com/s/VOY9Bprql6UfhKDIxYVptHbWA1?pwd=pjji#
「七星虚拟机」链接：https://pan.xunlei.com/s/VOYEPeKFTst6XWzYArT8HCa2A1?pwd=hqgu#
「电商图片采集工具」链接：https://pan.xunlei.com/s/VOYTyGNoQmx9ciEhFbMA1afdA1?pwd=zru2#
「场控助手」链接：https://pan.xunlei.com/s/VOYZ1P6cokb4EjBfQXAsjmo8A1?pwd=rkhe#
「TVBOX最新接口」链接：https://pan.xunlei.com/s/VOYdALqV30NTW53quTQfWHhmA1?pwd=beb8#
「AI唱歌软件AI翻唱Ai克隆自己声音唱任何人的歌曲效果超厉害」链接：https://pan.xunlei.com/s/VOYiL6cH2GCVrbv91FRy7uEZA1?pwd=whn8#
「SolidWorks2025最新完整版在此更新」链接：https://pan.xunlei.com/s/VOYnT0SsriDNDGjCciy_H67PA1?pwd=9jbk#
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
