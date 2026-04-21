# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# ===== Step 5: Add SEO tags to all posts =====
tag_script = r'''# -*- coding: utf-8 -*-
import pymysql
import re

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Define tag keywords and their auto-detection rules
tag_rules = [
    # Tag name -> keywords to detect in title
    ('AI教程', ['AI', 'ChatGPT', 'GPT', 'Midjourney', 'Stable Diffusion', 'Claude', '人工智能', 'Copilot', 'DALL-E', 'coze', '扣子']),
    ('影视资源', ['电影', '电视剧', '4K', '蓝光', '动漫', '番剧', '奥斯卡', 'BD', '全集', '韩剧', '美剧', '日剧']),
    ('音乐资源', ['音乐', 'DJ', 'mp3', '歌', '音频']),
    ('小说漫画', ['小说', '漫画', '同人', 'GL', '图书', '藏书']),
    ('PS教程', ['PS', 'Photoshop', '抠图', '字体特效', '合成']),
    ('编程开发', ['Java', 'Python', 'C#', 'HTML', 'CSS', 'MySQL', 'PHP', '编程', '前端', '后端', 'Web', '代码', '小程序']),
    ('设计教程', ['C4D', 'FCPX', 'AI软件', '平面设计', 'Dreamweaver', 'CorelDRAW', 'CDR', 'Solidworks', 'CAD']),
    ('短视频运营', ['抖音', '小红书', '哔哩', '短视频', '引流', '起号', '带货', '影视解说']),
    ('电商运营', ['淘宝', '拼多多', '闲鱼', '跨境电商', '开店', 'SHOPEE', '电商']),
    ('赚钱项目', ['赚钱', '副业', '创业', '月入', '百万', '富翁']),
    ('健康养生', ['中医', '养生', '补肾', '食疗', '健身']),
    ('破解软件', ['破解', '解锁', 'VIP', '修改版', '绿化', 'SVIP', 'Mod']),
    ('网盘工具', ['网盘', '迅雷', '百度网盘', 'UC网盘', '转存', '下载']),
    ('SEO教程', ['SEO', '搜索引擎', '排名']),
    ('维修教程', ['维修', '空调', '家电']),
    ('PPT模板', ['PPT', '简历', '模板']),
    ('游戏资源', ['游戏', '手游', '单机']),
    ('英语学习', ['英语', '四六级']),
    ('医学课程', ['医学', '临床']),
    ('职场技能', ['职场', '办公', 'WPS', 'Excel']),
]

# Get all posts
cursor.execute("SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID")
rows = cursor.fetchall()
print("Processing {} posts for tags...".format(len(rows)), flush=True)

# Ensure tag taxonomy exists
cursor.execute("SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE taxonomy='post_tag' LIMIT 1")
if not cursor.fetchone():
    print("No tag taxonomy found, creating...", flush=True)

# Create tags if not exist
tag_taxonomy_ids = {}
for tag_name, _ in tag_rules:
    # Check if tag exists
    cursor.execute("SELECT t.term_id FROM wp_terms t JOIN wp_term_taxonomy tt ON t.term_id=tt.term_id WHERE t.name=%s AND tt.taxonomy='post_tag'", (tag_name,))
    row = cursor.fetchone()
    if row:
        tag_taxonomy_ids[tag_name] = row[0]
        # Actually we need term_taxonomy_id
        cursor.execute("SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=%s AND taxonomy='post_tag'", (row[0],))
        tt_row = cursor.fetchone()
        if tt_row:
            tag_taxonomy_ids[tag_name] = tt_row[0]
    else:
        # Create tag
        slug = tag_name.lower().replace(' ', '-')
        cursor.execute("INSERT INTO wp_terms (name, slug) VALUES (%s, %s) ON DUPLICATE KEY UPDATE term_id=LAST_INSERT_ID(term_id)", (tag_name, slug))
        term_id = cursor.lastrowid
        cursor.execute("INSERT INTO wp_term_taxonomy (term_id, taxonomy, description, count) VALUES (%s, 'post_tag', '', 0)")
        tt_id = cursor.lastrowid
        tag_taxonomy_ids[tag_name] = tt_id
        conn.commit()
        print("Created tag: {}".format(tag_name), flush=True)

print("\nTags ready: {}".format(len(tag_taxonomy_ids)), flush=True)

# Assign tags to posts
tagged = 0
for post_id, title in rows:
    for tag_name, keywords in tag_rules:
        for kw in keywords:
            if kw.lower() in title.lower():
                tt_id = tag_taxonomy_ids[tag_name]
                # Check if already tagged
                cursor.execute("SELECT 1 FROM wp_term_relationships WHERE object_id=%s AND term_taxonomy_id=%s", (post_id, tt_id))
                if not cursor.fetchone():
                    cursor.execute("INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES (%s, %s, 0)", (post_id, tt_id))
                    cursor.execute("UPDATE wp_term_taxonomy SET count=count+1 WHERE term_taxonomy_id=%s", (tt_id,))
                break
    
    if (post_id - rows[0][0] + 1) % 100 == 0:
        conn.commit()
        print("Progress: {}/{}".format(post_id - rows[0][0] + 1, len(rows)), flush=True)

conn.commit()
conn.close()
print("\nDone! All posts tagged.", flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/seo_tags.py', 'w') as f:
    f.write(tag_script)
sftp.close()

print("Adding tags to all posts...", flush=True)
stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 seo_tags.py", timeout=300)
output = stdout.read().decode('utf-8', errors='replace').strip()
print(output, flush=True)

err = stderr.read().decode('utf-8', errors='replace').strip()
if err and 'error' in err.lower():
    print("ERR:", err[:300], flush=True)

ssh.close()
