# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

publish_script = r'''# -*- coding: utf-8 -*-
import pymysql
import time
import hashlib

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Categories: 影视娱乐=86, 教育资源=84, 工具合集=85, 自媒体运营=83
resources = [
    # Music (影视娱乐=86)
    {"title": "高品质车载DJ音乐大碟", "url": "https://drive.uc.cn/s/6b6622c1d37d4?public=1", "cat": 86},
    {"title": "精选音乐Mp3合集", "url": "https://drive.uc.cn/s/15e7b0d47d884", "cat": 86},
    # Tutorials (教育资源=84)
    {"title": "Html5+Css3由浅入深教程", "url": "https://drive.uc.cn/s/4b1848d6e36b4", "cat": 84},
    {"title": "黑帽SEO全套课程", "url": "https://drive.uc.cn/s/a5a5518113484", "cat": 84},
    {"title": "6天掌握MySQL基础视频教程", "url": "https://drive.uc.cn/s/4d9b7c9b416a4", "cat": 84},
    {"title": "最新C#零基础入门全集", "url": "https://drive.uc.cn/s/545c4bad670b4", "cat": 84},
    {"title": "JavaWeb新版全套教程", "url": "https://drive.uc.cn/s/04fd9d90bf654", "cat": 84},
    {"title": "Web前端全栈HTML5大神之路", "url": "https://drive.uc.cn/s/2f1e49b28a674", "cat": 84},
    {"title": "正则表达式入门教程", "url": "https://drive.uc.cn/s/e5179da8a5d74", "cat": 84},
    {"title": "FCPX全套资源", "url": "https://drive.uc.cn/s/383419a0c2694", "cat": 84},
    {"title": "记忆大师之李威教程 打造最强记忆", "url": "https://drive.uc.cn/s/f9e96afb1f7f4", "cat": 84},
    {"title": "PS 100款简易字体特效制作教程+源文件", "url": "https://drive.uc.cn/s/1208958b6fd94", "cat": 84},
    {"title": "C4D渲染器合集", "url": "https://drive.uc.cn/s/88809affa5454", "cat": 84},
    {"title": "平面设计速成 从小白到大神", "url": "https://drive.uc.cn/s/f33174c45c424", "cat": 84},
    {"title": "PS抠图0基础从入门到精通", "url": "https://drive.uc.cn/s/d444f96adca34", "cat": 84},
    {"title": "全套高清Photoshop收费教程", "url": "https://drive.uc.cn/s/144eaaa307314", "cat": 84},
    {"title": "AI软件系统教程 矢量魔法", "url": "https://drive.uc.cn/s/1500f5a08f744", "cat": 84},
    {"title": "电商合成案例教程 掌握合成技法", "url": "https://drive.uc.cn/s/5458d031f4cc4", "cat": 84},
    {"title": "某宝买的PS资源合集", "url": "https://drive.uc.cn/s/e0148855f0dd4", "cat": 84},
    {"title": "JAVA基础到高级全套教程", "url": "https://drive.uc.cn/s/3a02d35a08244", "cat": 84},
    {"title": "Python全套教程", "url": "https://drive.uc.cn/s/786079f453dc4", "cat": 84},
    {"title": "Dreamweaver CC网页设计从入门到精通", "url": "https://drive.uc.cn/s/f7b84e2f7d5a4", "cat": 84},
    {"title": "小程序开发教程大合集 零基础到精通", "url": "https://drive.uc.cn/s/5e7c7ed278b04", "cat": 84},
    {"title": "2025医学类视频课程合集", "url": "https://drive.uc.cn/s/fec141e4b2394", "cat": 84},
    {"title": "16节实用性爆棚的PS教学 走进Photoshop CC", "url": "https://drive.uc.cn/s/781b0df66f524", "cat": 84},
    {"title": "英语四六级保命班", "url": "https://drive.uc.cn/s/0b3f5fbf37c84", "cat": 84},
    {"title": "瑞思拜四六级讲义（12月考试）", "url": "https://drive.uc.cn/s/b58cb4261b5e4", "cat": 84},
    # Tools (工具合集=85)
    {"title": "电脑工具合集", "url": "https://drive.uc.cn/s/af1d7a0351a54", "cat": 85},
    {"title": "游戏内购合集资源", "url": "https://drive.uc.cn/s/7f7b570ae8ef4", "cat": 85},
    {"title": "软件合集", "url": "https://drive.uc.cn/s/759efdc1128a4", "cat": 85},
    # Self Media (自媒体运营=83)
    {"title": "淘宝开店教程100节课", "url": "https://drive.uc.cn/s/b0f8461696e74", "cat": 83},
    {"title": "抖音引流课程 日引300粉实战", "url": "https://drive.uc.cn/s/6e0472d6fb964", "cat": 83},
    {"title": "哔哩实操运营 从0到20万粉", "url": "https://drive.uc.cn/s/6c2d2a9040204", "cat": 83},
    {"title": "抖音电商 小红书电商最新玩法", "url": "https://drive.uc.cn/s/c553800a1e144", "cat": 83},
    # Movies/TV (影视娱乐=86)
    {"title": "最新电影TOP250部", "url": "https://drive.uc.cn/s/ab7dabef14d54", "cat": 86},
    {"title": "最新电视剧合集", "url": "https://drive.uc.cn/s/a03939f22d294", "cat": 86},
    {"title": "第95届奥斯卡电影合集", "url": "https://drive.uc.cn/s/b4fbc1389e4a4", "cat": 86},
    {"title": "莉可莉丝 Lycoris Recoil BD全集", "url": "https://drive.uc.cn/s/0f04e2e70f3a4", "cat": 86},
    {"title": "首尔之春 蓝光原盘REMUX", "url": "https://drive.uc.cn/s/089d02ae8ef04", "cat": 86},
    # Novels/Manga (影视娱乐=86)
    {"title": "高分小说600本合集", "url": "https://drive.uc.cn/s/835d774f83a84", "cat": 86},
    {"title": "动情小说GL合集590本", "url": "https://drive.uc.cn/s/86bed2af8adf4", "cat": 86},
    {"title": "同人漫画合集", "url": "https://drive.uc.cn/s/740f6eb0c39a4", "cat": 86},
]

# Check duplicates
published_titles = set()
cursor.execute("SELECT post_title FROM wp_posts WHERE post_type='post' AND post_status='publish'")
for row in cursor.fetchall():
    published_titles.add(row[0])

to_publish = []
for res in resources:
    found = any(res["title"][:6] in pt or pt[:6] in res["title"] for pt in published_titles)
    if not found:
        to_publish.append(res)

print("Total: {}, Already: {}, To publish: {}".format(len(resources), len(resources)-len(to_publish), len(to_publish)))

cat_names = {86: "影视娱乐", 84: "教育资源", 85: "工具合集", 83: "自媒体运营"}

for i, res in enumerate(to_publish):
    title = res["title"]
    url = res["url"]
    cat = res["cat"]
    ts = str(int(time.time()))
    slug = "uc-{}-{}".format(ts, hashlib.md5(title.encode()).hexdigest()[:4])
    cat_name = cat_names.get(cat, "其他")

    content_html = (
        '<p>资源名称：{title}</p>'
        '<p>资源类型：{cat_name}</p>'
        '<p>📁 网盘来源：UC网盘</p>'
        '<p>⭐ <strong>使用方法：</strong>复制链接 → 打开浏览器 → 登录UC网盘 → 保存到自己的网盘即可使用</p>'
        '<p>下载链接：<a href="{url}" target="_blank" rel="noopener">{url}</a></p>'
        '<p>⚠️ 资源来源于网络，仅供学习娱乐使用，禁止商用。如有侵权请联系删除。</p>'
    ).format(title=title, url=url, cat_name=cat_name)

    try:
        cursor.execute(
            "INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,"
            "post_excerpt,post_status,comment_status,ping_status,post_name,to_ping,pinged,"
            "post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,"
            "post_type,post_mime_type,comment_count) "
            "VALUES (1,NOW(),UTC_TIMESTAMP(),%s,%s,'','publish','closed','closed',%s,"
            "'','',NOW(),UTC_TIMESTAMP(),'',0,%s,0,'post','',0)",
            (content_html, title, slug, "https://skillxm.cn/?p=0")
        )
        post_id = cursor.lastrowid
        cursor.execute("UPDATE wp_posts SET guid='https://skillxm.cn/?p={}' WHERE ID={}".format(post_id, post_id))
        cursor.execute("INSERT INTO wp_term_relationships (object_id,term_taxonomy_id,term_order) VALUES ({},{},0)".format(post_id, cat))
        cursor.execute("UPDATE wp_term_taxonomy SET count=count+1 WHERE term_taxonomy_id={}".format(cat))
        conn.commit()
        print("[{}/{}] OK ID:{} {}".format(i+1, len(to_publish), post_id, cat_name), flush=True)
        time.sleep(0.3)
    except Exception as e:
        conn.rollback()
        print("[{}/{}] FAIL: {} - {}".format(i+1, len(to_publish), title, e), flush=True)

conn.close()
print("\nDone!", flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/publish_uc.py', 'w') as f:
    f.write(publish_script)
sftp.close()

print("Script uploaded. Publishing 42 UC resources...", flush=True)

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 publish_uc.py", timeout=180)
output = stdout.read().decode('utf-8', errors='replace')
print(output, flush=True)

ssh.close()
