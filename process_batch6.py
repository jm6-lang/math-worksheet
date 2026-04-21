#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章 - 第六批"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

raw_data = """
「国漫心动的声音」链接：https://pan.xunlei.com/s/VOOaNI3XfMGla7ryiVqmjeh2A1
「国漫一醉经年」链接：https://pan.xunlei.com/s/VOOaLLaebOjliyh3J4n57KFrA1
「海外动漫大合集」链接：https://pan.xunlei.com/s/VOQ6HmfTqOKXA42tDmbjtuHRA1?pwd=mi6x#
「动漫影视」链接：https://pan.xunlei.com/s/VOQ6INjfEA2Y8YjpMwYDCF93A1?pwd=2qmt#
「爆燃动漫剪辑」链接：https://pan.xunlei.com/s/VOQBYxq24u-CygjX9Tcm0_vaA1?pwd=g9vy#
「超全音乐合集」链接：https://pan.xunlei.com/s/VOQ6EmI-iQ_8twVbXwFaP3siA1?pwd=bmzr#
「上万首音乐合集」链接：https://pan.xunlei.com/s/VOQ6F5Yc2esiP0XWBKwJilRRA1?pwd=vqud#
「003车载高清MV持续更新」链接：https://pan.xunlei.com/s/VOQ6FJquhmy4r_XKAnK9GkWqA1?pwd=wx67#
「经典老歌1020首」链接：https://pan.xunlei.com/s/VOQ6JtR3TsH5kZ03S1gE8TPWA1?pwd=pf6k#
「零基础学唱粤语歌曲KTV」链接：https://pan.xunlei.com/s/VOQ6K-KHNSmMb1YsHO_RG5U5A1?pwd=6kmd#
「office全套学习资料办公室一族必备」链接：https://pan.xunlei.com/s/VOOaLurmDvaNOzRoOLlxQu97A1?pwd=bzmd#
「创业副业引流必备」链接：https://pan.xunlei.com/s/VOOaMBk3aNeIhBhmUKznB4VvA1?pwd=mtj5#
「剪映预设专场+蒙版+调色合集」链接：https://pan.xunlei.com/s/VOOaMF1xtx2hjdy5BesUfrv4A1?pwd=9hv2#
「瑜伽从初级到高级100课」链接：https://pan.xunlei.com/s/VOOeoLyukJX_aZwoiNkWleI7A1?pwd=bzjp#
「小学初中教辅资料合集」链接：https://pan.xunlei.com/s/VOOetwrUNr60xSX58xAhyVOwA1?pwd=nhin#
「素材库合集音频音效视频CG图片」链接：https://pan.xunlei.com/s/VOOeu6UWYpy8J5er-4UwSJDjA1
「电工技术自学一本通」链接：https://pan.xunlei.com/s/VOOk9yp5rK69yZ7BxcLcQmvtA1?pwd=qz73#
「全新手机维修课程合集」链接：https://pan.xunlei.com/s/VOOkA4PFdxoVSJw1VI9gXX--A1?pwd=ytaf#
「推拿手法技能中医护理」链接：https://pan.xunlei.com/s/VOOkAt1C_mrrD5nVVcf7R4naA1?pwd=wmtf#
「零基础化妆入门课程」链接：https://pan.xunlei.com/s/VOOkB-rFnr_4W6s7-XT9hDpkA1?pwd=dfe8#
「陈式太极拳视频教程」链接：https://pan.xunlei.com/s/VOOuKnMFlFjUlpMDhOty4N25A1?pwd=ac94#
「小红书图文批量生成」链接：https://pan.xunlei.com/s/VOOuLP7RcTHXBSgoQ8TUE9u5A1?pwd=y5ey#
「木工雕刻学习课程」链接：https://pan.xunlei.com/s/VOOuLibJYdubhdMd9PHS0dSGA1?pwd=ua49#
「老中医的传世小偏方经典老偏方全家都能用的日常小病治疗秘方」链接：https://pan.xunlei.com/s/VOOuLxqpkJX_aZwoiNkd1ABcA1?pwd=jszc#
「家庭实用菜谱家庭自制美味辣酱下饭辣酱制作pdf」链接：https://pan.xunlei.com/s/VOOuM32D4_-Pa6ix4UC9NF-YA1?pwd=dn96#
「60种编程语言学习书籍」链接：https://pan.xunlei.com/s/VOP3plym1uIGNBJn5Z3gGQP4A1?pwd=qkn9#
「人人有用的零基础理财入门课」链接：https://pan.xunlei.com/s/VOP3qirJQOdVHsoV-juXOSLJA1?pwd=xwbm#
「零基础学剪映」链接：https://pan.xunlei.com/s/VOP3qubpQVZ1ur1_zvuQE3zEA1?pwd=mwc8#
「零基础学唱歌」链接：https://pan.xunlei.com/s/VOP3r1GPeb6v-im-wVm3VuSSA1?pwd=ynhr#
「零基础学炒股」链接：https://pan.xunlei.com/s/VOP3rBMsNUlzBbd7cRYvoK_7A1?pwd=2izj#
「零基础学航拍」链接：https://pan.xunlei.com/s/VOP3rIlTNUlzBbd7cRYvoMgbA1?pwd=2t78#
「零基础摄影班」链接：https://pan.xunlei.com/s/VOP3rRY7cT3EWLjpt5L_S4WGA1?pwd=embc#
「零基础学手语」链接：https://pan.xunlei.com/s/VOP3rYTukWzziTqwUC0y_PoFA1?pwd=safr#
「零基础学绘画」链接：https://pan.xunlei.com/s/VOP3rdYA3WwJwAbr3_ZNNM-fA1?pwd=3yec#
「恋爱修炼秘籍」链接：https://pan.xunlei.com/s/VOP3s7G4eHRZY2IUihc2W4QTA1?pwd=m9bj#
「成人修炼手册」链接：https://pan.xunlei.com/s/VOP3sG8COZ7sHno8EpjIv6eyA1?pwd=zzz9#
「正妹博士性学教室男女那些羞羞事」链接：https://pan.xunlei.com/s/VOP3sN3WRLFd38dbpR7EvtPoA1?pwd=pjga#
「爱爱技巧」链接：https://pan.xunlei.com/s/VOP3sStc1dckpi3HngYIQBEGA1?pwd=9335#
「SVIP房中技巧班高级研修班」链接：https://pan.xunlei.com/s/VOP3sqXERLFd38dbpR7Ew2dUA1?pwd=xhkt#
「吴小飘15堂G点愉悦手册打开高巢新世界完结」链接：https://pan.xunlei.com/s/VOP4439m8veTkcQsuuxTDzHfA1?pwd=hw2g#
「男性x技宝典14招实战Y女术爱抚按摩C情姿势G潮全攻略」链接：https://pan.xunlei.com/s/VOP44rwnFXPj87MPK2PWwnuSA1?pwd=bgwe#
「公司文员必存资源」链接：https://pan.xunlei.com/s/VOQ6FBWvNSmMb1YsHO_REEqUA1?pwd=3g3n#
「钓鱼视频教程实战大全技巧」链接：https://pan.xunlei.com/s/VOQ6K54BUcNz3Mu_oHtAebFcA1?pwd=9xyj#
「计算机考证课程」链接：https://pan.xunlei.com/s/VOQ6KRJJPV5TjTtqcfU8aDB7A1?pwd=k25j#
「2024女性必备的20堂情趣指南课完结」链接：https://pan.xunlei.com/s/VOQ6KYFJOM4F_E1Lcbt86a6MA1?pwd=ay24#
「女生呵护指南」链接：https://pan.xunlei.com/s/VOQ6KdJB7MK-8MadlJlaxUbtA1?pwd=297e#
「李银河这才是你想要的性」链接：https://pan.xunlei.com/s/VOQ6Kt9-LVQRsktvQtBSUTdjA1?pwd=rn95#
「按摩教学」链接：https://pan.xunlei.com/s/VOQ6LX14udm-6ik46ZifNZOkA1?pwd=x62q#
「医学课程」链接：https://pan.xunlei.com/s/VOQ6M187aY8k8FITC81_h0zEA1?pwd=txdg#
「教资」链接：https://pan.xunlei.com/s/VOQ6M9e8DzxF93hrLeszFuS9A1?pwd=5gi7#
「美丽芭蕾孕期特辑」链接：https://pan.xunlei.com/s/VOQ6N8Wl829Ak4YZiGHD686aA1?pwd=m5xq#
「如何辨别渣男渣女训练营一套成神」链接：https://pan.xunlei.com/s/VOQBYCnJcn-7E-aYxlZZT0AJA1?pwd=z42e#
「微信机器人工具+视频教程」链接：https://pan.xunlei.com/s/VOQBYMouy5qFuBJcHF8Opc-yA1?pwd=wch8#
「最新剪映从入门到精通100课网红都学过」链接：https://pan.xunlei.com/s/VOQBZ9_kWkj3fzJHr6mj76i4A1?pwd=sm8i#
「国际象棋入门教程」链接：https://pan.xunlei.com/s/VOQBZOdbLnlUbHA45Jg4GN4FA1?pwd=adyz#
「扑克牌千术揭秘十赌九骗」链接：https://pan.xunlei.com/s/VOQBZfk-Cu0rmDZIdzUW2wcgA1?pwd=4kjj#
「围棋入门课程大全」链接：https://pan.xunlei.com/s/VOQB_QhgUGArPcbdUIa6wLE9A1?pwd=ss7j#
「书法教程教你零基础写出一手漂亮好字完结」链接：https://pan.xunlei.com/s/VOQB_XeOc5OUVTauZez_fwDUA1?pwd=77ez#
「用科学的心理学通识看透人性」链接：https://pan.xunlei.com/s/VOQB_osJCu0rmDZIdzUW3KrCA1?pwd=pb2e#
「日语零基础直达N1」链接：https://pan.xunlei.com/s/VOU7snTWH66jxoSBFoNZopvAA1?pwd=4kfa#
「U盘重装系统到电脑系统维护维修视频」链接：https://pan.xunlei.com/s/VOYJVgSoUAhvX4E4C5QPoo0wA1?pwd=7khq#
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
