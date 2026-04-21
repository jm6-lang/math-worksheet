#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析网盘链接并批量匹配更新文章"""
import paramiko, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# 用户提供的链接数据（自媒体电商类+教育类）
raw_data = """
「【小红书】玩法教程最全攻略【24套课】」链接：https://pan.quark.cn/s/cb0de89979a8
「【TikTok】玩法教程最全攻略【27套课】」链接：https://pan.quark.cn/s/44a65ca8c8cd
「【抖音】玩法教程最全攻略【21套课】」链接：https://pan.quark.cn/s/f17ab4fd435d
「小红书带货42天训练营无压货」链接：https://pan.quark.cn/s/60e57dc22ac8
「电商课程·拼多多运营必听10节课」链接：https://pan.quark.cn/s/b486d9d3c3d7
「旅行小红书起号运营，深入浅出为大家讲解旅行在小红书如何起号、涨粉、引流、变现」链接：https://pan.quark.cn/s/b6406d8001a1
「跨境电商实操课程从零到精通，人人都适合的跨境电商课 小二郎资源库每日更新」链接：https://pan.quark.cn/s/d09808093993
「小红书爆款文案【指令+教程】」链接：https://pan.quark.cn/s/a0eb204cecb7
「影视解说训练营，从新手进阶到成熟自媒体达人」链接：https://pan.quark.cn/s/74d6f6d286e4
「起号：给自媒体人的60条实操干货」链接：https://pan.quark.cn/s/9ad9f6c8a9cf
「新媒体流量变现运营课程」链接：https://pan.quark.cn/s/af324f13eeaf
「阿里巴巴国际站课程，阿里巴巴国际站运营基础课程」链接：https://pan.quark.cn/s/9f32d229f7f0
「TikTok海外影视课程全套」链接：https://pan.quark.cn/s/fd97bad234ed
「外贸线上实战训练营」链接：https://pan.quark.cn/s/b6782807e7da
「带货短视频文案脚本公式进阶班」链接：https://pan.quark.cn/s/bd65e40662fa
「《从流量到留量：让你的产品实现低成本持续增长》」链接：https://pan.quark.cn/s/7bf2401503bd
「【生财有术】上千条付费资源合集」链接：https://pan.quark.cn/s/5cb9b0429874
「视频号风口21天从0到1视频课程」链接：https://pan.quark.cn/s/22dad9ef0225
「视频号运营实战课程」链接：https://pan.quark.cn/s/0637528c7bd1
「【公众号运营】零基础入门公众号全方位讲解」链接：https://pan.quark.cn/s/0b22c3599f3b
「付费群流出写作教程【16合集】」链接：https://pan.quark.cn/s/0177baad81d4
「2025一建二建全科各机构最新网课」链接：https://pan.quark.cn/s/349bbce69e86
「销售营销学顶级精英教学视频课程【18套】」链接：https://pan.quark.cn/s/749dd7db6608
「孩子必听的100个历史故事（完结）」链接：https://pan.quark.cn/s/260d646d91d5
「孕期全攻略（完结）」链接：https://pan.quark.cn/s/1de29234509d
「全球外语最新精整26门小语种零基础全套学习资料」链接：https://pan.quark.cn/s/f67180336b4e
「雪梨老师学英语，自然拼读音标课语法课新概念全套【80GB】」链接：https://pan.quark.cn/s/37db7af0aad7
「我不是教你玩阴的：鬼谷子的心理学诡计」链接：https://pan.quark.cn/s/fd1d8a5e21a9
「【最新版公考面试课程】」链接：https://pan.quark.cn/s/ba2cb4ccc858
「十三天快速通关高中历史」链接：https://pan.quark.cn/s/9618fa92528a
「000超级记忆力训练课程（16天）」链接：https://pan.quark.cn/s/00fa9188dd84
「国考公考省考资料合辑（2024-2025）」链接：https://pan.quark.cn/s/3ff435f62136
「2025考研英语词汇闪过（10本）」链接：https://pan.quark.cn/s/1e01ab58bdaf
「2025年7节课搞定国考常识」链接：https://pan.quark.cn/s/d5ed5281d50c
「初中各科知识点梳理」链接：https://pan.quark.cn/s/74153e93c83e
「高中教辅资源汇总合集」链接：https://pan.quark.cn/s/4807ab495ed8
「雅思旗舰VIP直达7分班」链接：https://pan.quark.cn/s/4d63fc4a67d1
「2025年考研复试必备资料（复试流程+英语+专业课）」链接：https://pan.quark.cn/s/6f91441b54ef
「初中九科学霸笔记（无水印）」链接：https://pan.quark.cn/s/79183bb66cc5
「初级社工教材（2025年）」链接：https://pan.quark.cn/s/9de8457192dc
「中级社工教材（2025年）」链接：https://pan.quark.cn/s/7f8f7bf7076d
「法考资料（2025年）」链接：https://pan.quark.cn/s/25eaee3c01c2
「乔伯伯5500词汇系统英语课 (127节)」链接：https://pan.quark.cn/s/fe1f2edbbb28
「2025自考+专升本+学位英语合集」链接：https://pan.quark.cn/s/cf39d8b82e38
「985学霸逆袭学习方法+提分经验」链接：https://pan.quark.cn/s/6c1fc54308ad
「高考能力提升卷」链接：https://pan.quark.cn/s/873a9bb68de4
「相命学课程全集」链接：https://pan.quark.cn/s/6df1ce12f8c3
「考神大牛韩语零基础0-TOPIK4全程班」链接：https://pan.quark.cn/s/9fdfb7c2b17e
「启蒙英语动画」链接：https://pan.quark.cn/s/58476c46e35e
「可打印教育资源合集」链接：https://pan.quark.cn/s/9d3a3de94c1d
"""

# 解析链接
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

# 保存链接JSON
links_json = json.dumps(entries, ensure_ascii=False)

# 连接服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 上传链接JSON
sftp = ssh.open_sftp()
links_file = '/tmp/links_batch.json'
with sftp.open(links_file, 'w') as f:
    f.write(links_json)
sftp.close()

# 执行匹配脚本
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
    
    # 1. 精确匹配
    if link_title in articles:
        found_id = articles[link_title]
    
    # 2. 包含匹配
    if not found_id:
        for art_title, art_id in articles.items():
            if link_title in art_title or art_title in link_title:
                found_id = art_id
                break
    
    # 3. 模糊匹配
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

err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print(f"错误: {err}")

# 清理
ssh.exec_command("rm /tmp/links_batch.json")
ssh.close()
print("\n处理完成。继续发下一批吧。")
