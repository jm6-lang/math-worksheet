#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第四批"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「漫画合集168部304GB」链接：https://pan.quark.cn/s/2ecdc523b7b2
「国漫秦时明月全6季国语中字4K」链接：https://pan.quark.cn/s/a434864fa08e
「小说合集1」链接：https://pan.quark.cn/s/4011f86fae7f
「小说合集2」链接：https://pan.quark.cn/s/62acf4a6f4aa
「上万本小说合集3」链接：https://pan.quark.cn/s/46969ebc99ea
「画江湖之不良人1-6季全集」链接：https://pan.quark.cn/s/a1eb2634adee
「约hui大作战S1+S2+S3+S4赤黑新章前后」链接：https://pan.quark.cn/s/775379475ef0
「动漫合集欧美日本」链接：https://pan.quark.cn/s/02d6b35340ac
「民间故事合集素材」链接：https://pan.quark.cn/s/2c9e92fdcfdc
「无限流小说102部合集」链接：https://pan.quark.cn/s/cc15779bc56c
「日漫电影」链接：https://pan.quark.cn/s/a85fe781526f
「L灵珑第二季」链接：https://pan.quark.cn/s/2994fbf0fe4d
「宫崎骏电影系列合集」链接：https://pan.quark.cn/s/3b76fde794a1
「爱死机」链接：https://pan.quark.cn/s/72efb403ca15
「漫画屋」链接：https://pan.quark.cn/s/aec95a35f1ee
「动漫合集库」链接：https://pan.quark.cn/s/29af05b1591e
「Reface一键换脸 v4.5.0 AI换脸工具」链接：https://pan.quark.cn/s/a54960efcf08
「上班摸鱼老板键软件」链接：https://pan.quark.cn/s/19ea6c40d155
「Listen1全网音乐免费听」链接：https://pan.quark.cn/s/0f19852eab83
「Autodesk AutoCAD 2024」链接：https://pan.quark.cn/s/648e797ff85b
「酒店防窥检测1.26解锁会员版」链接：https://pan.quark.cn/s/a55f9d261f02
「去水印工具」链接：https://pan.quark.cn/s/24d6f26bb2d0
「AI Chat」链接：https://pan.quark.cn/s/3ebb19f720cc
「驾考题库大全会员版」链接：https://pan.quark.cn/s/9394c429b093
「呐噗助眠」链接：https://pan.quark.cn/s/8e95a99ab039
「嗅觉浏览器」链接：https://pan.quark.cn/s/e159f31feb5e
「扫描全能王解锁付费版」链接：https://pan.quark.cn/s/9f1a2cb69dcd
「洛雪音乐附最新可用音源」链接：https://pan.quark.cn/s/7d199c18f040
「全新推出的免费音乐听歌软件尼卡音乐」链接：https://pan.quark.cn/s/852813bc1eb9
「车机」链接：https://pan.quark.cn/s/1828d0268644
「漫漫漫画v5.2.43为广大漫画爱好者打造的追漫神器去广告版」链接：https://pan.quark.cn/s/2c9aa2031ed5
「手机照片恢复管家7.5.0 VIP版」链接：https://pan.quark.cn/s/6eb35751e6d1
「福昕高级PDF编辑器」链接：https://pan.quark.cn/s/88398fa94928
「微信对话生成器」链接：https://pan.quark.cn/s/e681e222ae6c
「傻瓜英语VIP解锁版」链接：https://pan.quark.cn/s/0f69354ca70f
「酷我音乐破解版兼容所有机型解锁SVIP支持鸿蒙」链接：https://pan.quark.cn/s/2921e8a1b59c
「Windows系统永久激活最新密钥」链接：https://pan.quark.cn/s/275d58007c5e
「畅听FM2.3.2可收听全国电台免费无广告」链接：https://pan.quark.cn/s/b7046489b6b0
「Android健身教练v1.1.5免费无广告」链接：https://pan.quark.cn/s/1826d7020682
「开发全能工具箱He3」链接：https://pan.quark.cn/s/44ead176505a
「情侣飞行棋先保存防和谐」链接：https://pan.quark.cn/s/e7686d3af590
「万能格式转换」链接：https://pan.quark.cn/s/bc01151338ab
「解析机器人破解版」链接：https://pan.quark.cn/s/1a7eb2d5e97c
「GET漫画v2.1.1绿化版」链接：https://pan.quark.cn/s/7ecfc9951415
「任小聊天话术APP」链接：https://pan.quark.cn/s/b3f5ed71e705
「视频音频批量格式转换器v2.0」链接：https://pan.quark.cn/s/504ba86954a3
「微信聊天恢复4.6.0」链接：https://pan.quark.cn/s/422a8656030e
「万象聚搜v1.5增小说漫画视频去水印等功能」链接：https://pan.quark.cn/s/e5d3418ec0c1
「风云录屏大师VIP版无水印无广告高清录屏工具」链接：https://pan.quark.cn/s/0cb1bbec039c
「视频去重」链接：https://pan.quark.cn/s/ccee65cc166f
「黑神话悟空」链接：https://pan.quark.cn/s/bf63e69e7ac4
「AutoGLM」链接：https://pan.quark.cn/s/2846843621eb
「博看书苑安卓附36个授权码」链接：https://pan.quark.cn/s/a2daac82453e
「夸父工具箱」链接：https://pan.quark.cn/s/dc45d88e2e97
「工具魔盒2.4.2」链接：https://pan.quark.cn/s/cdce324e9439
「安卓解析机器人高级版」链接：https://pan.quark.cn/s/e9e7a37395af
「太极工具箱」链接：https://pan.quark.cn/s/d8647b53e016
「快影剪辑纯净版」链接：https://pan.quark.cn/s/de8c3c44f755
「Xmind思维导图模板331个」链接：https://pan.quark.cn/s/b31c5d0863d5
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
