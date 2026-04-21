# -*- coding: utf-8 -*-
# Publish 22 missing resources to WordPress
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

# Category: 工具合集=85, 教育资源=84
resources = [
    # Books that may be missing (教育资源=84)
    {"title": "中国古玩鉴识知识系列书籍", "url": "https://pan.xunlei.com/s/VOOk9ly0JBu9rQyGiwv31UsnA1?pwd=uy8e#", "cat": 84, "type": "book"},
    {"title": "创业优质教程合集", "url": "https://pan.xunlei.com/s/VOOuKbEkRTmQCQcZcBrRvcYtA1?pwd=y96q#", "cat": 84, "type": "book"},
    {"title": "百病食疗大全（彩图精装）", "url": "https://pan.xunlei.com/s/VOOuKiYOFPUtXUKuIOgMhb4yA1?pwd=nidc#", "cat": 84, "type": "book"},
    {"title": "用声音修炼气场（完结）", "url": "https://pan.xunlei.com/s/VOOuLYoTRTmQCQcZcBrRvzs-A1?pwd=2xtq#", "cat": 84, "type": "book"},
    {"title": "梅花易数白话解", "url": "https://pan.xunlei.com/s/VOOuLe65NaBNlzRDdqMF43NUA1?pwd=kk74#", "cat": 84, "type": "book"},
    {"title": "富爸爸系列全集（纪念新版·共32册）", "url": "https://pan.xunlei.com/s/VOP3rnoD-wEAtCmsdBlggRXRA1?pwd=4m5x#", "cat": 84, "type": "book"},
    {"title": "书库合集", "url": "https://pan.xunlei.com/s/VOQ6I4rzezacrOCmZ3xzNozIA1?pwd=dmnj#", "cat": 84, "type": "book"},
    {"title": "人人都可以学的顶级思维法（套装共7册）", "url": "https://pan.xunlei.com/s/VOQ6KC01-caw75eeiJRzVHXPA1?pwd=2474#", "cat": 84, "type": "book"},
    {"title": "富爸爸套装五册", "url": "https://pan.xunlei.com/s/VOQ6KI9A7MK-8MadlJlaxMUgA1?pwd=re3g#", "cat": 84, "type": "book"},
    {"title": "中医补肾壮阳秘方", "url": "https://pan.xunlei.com/s/VOQ6MNnRpklQNxGL9FDLjXYdA1?pwd=wqx2#", "cat": 84, "type": "book"},
    {"title": "父与子的X教尬聊", "url": "https://pan.xunlei.com/s/VOQ6Mi03829Ak4YZiGHD5x7yA1?pwd=cy93#", "cat": 84, "type": "book"},
    {"title": "MBA课程", "url": "https://pan.xunlei.com/s/VOQ6MoEjeF5hzjNz8XoKo6nVA1?pwd=mv75#", "cat": 84, "type": "book"},
    {"title": "中医古籍合集超全系列", "url": "https://pan.xunlei.com/s/VOQBckc4OoRRo7e7hTVWQymaA1?pwd=7fqn#", "cat": 84, "type": "book"},
    {"title": "农村自建房图纸合集", "url": "https://pan.xunlei.com/s/VOVjp6cmrCI1e6xO09VM77mAA1?pwd=emit#", "cat": 84, "type": "book"},
]

# Tools (工具合集=85)
tool_resources = [
    {"title": "夸克网盘批量转存分享工具", "url": "https://pan.xunlei.com/s/VOQ6LIBchwbqjdXwYUw4zaeBA1?pwd=n8hd#", "cat": 85},
    {"title": "轻听音乐v2.2.6免费版", "url": "https://pan.xunlei.com/s/VOWcbhIhc3ogRlnOhWz16z-lA1?pwd=3nbk#", "cat": 85},
    {"title": "全球卫星电视TV garden", "url": "https://pan.xunlei.com/s/VOWrpwtWTK_RkTvQWYTGJ2pJA1?pwd=s8a8#", "cat": 85},
    {"title": "即梦Ai破解版无限积分", "url": "https://pan.xunlei.com/s/VOWrq9oLeoQT89x8UX6ZS-cFA1?pwd=h48t#", "cat": 85},
    {"title": "动物翻译器", "url": "https://pan.xunlei.com/s/VOWrqDLfYa-Iuq5t6PKsOHgYA1?pwd=fi2t#", "cat": 85},
    {"title": "搬运工具包", "url": "https://pan.xunlei.com/s/VOX6JDhMOOp5Lb8QDfV7mxp4A1?pwd=cx78#", "cat": 85},
    {"title": "电脑密码破解工具", "url": "https://pan.xunlei.com/s/VOXBRniSZWYhuK2DRAmIJ3HLA1?pwd=gy5h#", "cat": 85},
    {"title": "手机版闲鱼助手自动发货", "url": "https://pan.xunlei.com/s/VOXGks0nYB0jDG4ROtTuoiJ0A1?pwd=edim#", "cat": 85},
    {"title": "图片批量处理", "url": "https://pan.xunlei.com/s/VOXW6jHtze9Rl3yZAc9OfK0tA1?pwd=6qcd#", "cat": 85},
    {"title": "文件批量重命名", "url": "https://pan.xunlei.com/s/VOXW6r92yNaOLWrUcv2qljKzA1?pwd=7hza#", "cat": 85},
    {"title": "手机刷机工具箱", "url": "https://pan.xunlei.com/s/VOXaFh7CRwAxaJVLO94ZJrKiA1?pwd=ppf6#", "cat": 85},
    {"title": "CDR2023中文破解版CorelDRAW", "url": "https://pan.xunlei.com/s/VOXfSJnKcx4UdHEqZS9f5viOA1?pwd=2z4i#", "cat": 85},
    {"title": "打卡软件神器", "url": "https://pan.xunlei.com/s/VOXumZU5y-6A2bPiWO5dRzkrA1?pwd=88aq#", "cat": 85},
    {"title": "查企业查信息（送5年SVIP）", "url": "https://pan.xunlei.com/s/VOY--vv8UsLDxjyOGMSyLOd5A1?pwd=48gy#", "cat": 85},
    {"title": "笔趣阁完美修改去广告解锁高级版", "url": "https://pan.xunlei.com/s/VOY42lVZqub9V_5XZd13WCacA1?pwd=g4yv#", "cat": 85},
    {"title": "公众号爆文机器人", "url": "https://pan.xunlei.com/s/VOY9Bprql6UfhKDIxYVptHbWA1?pwd=pjji#", "cat": 85},
    {"title": "七星虚拟机", "url": "https://pan.xunlei.com/s/VOYEPeKFTst6XWzYArT8HCa2A1?pwd=hqgu#", "cat": 85},
    {"title": "电商图片采集工具", "url": "https://pan.xunlei.com/s/VOYTyGNoQmx9ciEhFbMA1afdA1?pwd=zru2#", "cat": 85},
    {"title": "场控助手", "url": "https://pan.xunlei.com/s/VOYZ1P6cokb4EjBfQXAsjmo8A1?pwd=rkhe#", "cat": 85},
    {"title": "TVBOX+最新接口", "url": "https://pan.xunlei.com/s/VOYdALqV30NTW53quTQfWHhmA1?pwd=beb8#", "cat": 85},
    {"title": "AI唱歌软件·AI翻唱克隆声音", "url": "https://pan.xunlei.com/s/VOYiL6cH2GCVrbv91FRy7uEZA1?pwd=whn8#", "cat": 85},
    {"title": "SolidWorks2025最新完整版", "url": "https://pan.xunlei.com/s/VOYnT0SsriDNDGjCciy_H67PA1?pwd=9jbk#", "cat": 85},
]

all_resources = resources + tool_resources

# Check for duplicates first - skip already published
published_titles = set()
cursor.execute("SELECT post_title FROM wp_posts WHERE post_type='post' AND post_status='publish'")
for row in cursor.fetchall():
    published_titles.add(row[0])

to_publish = []
for res in all_resources:
    title = res["title"]
    # Check if already exists (fuzzy match)
    found = False
    for pt in published_titles:
        # Check if key words match
        key = title[:6]
        if key in pt or pt[:6] in title:
            found = True
            break
    if not found:
        to_publish.append(res)

print("Total resources: {}".format(len(all_resources)))
print("Already published: {}".format(len(all_resources) - len(to_publish)))
print("To publish: {}".format(len(to_publish)))

for i, res in enumerate(to_publish):
    title = res["title"]
    url = res["url"]
    cat = res["cat"]
    prefix = "book" if res.get("type") == "book" else "res"
    
    ts = str(int(time.time()))
    slug = "{}-{}-{}".format(prefix, ts, str(hashlib.md5(title.encode()).hexdigest()[:4]))
    
    content_html = """<p>资源名称：{title}</p>
<p>资源类型：{cat_name}</p>
<p>下载链接：<a href="{url}" target="_blank">{url}</a></p>
<p>温馨提示：复制链接后打开迅雷查看，如链接失效请留言反馈。</p>""".format(
        title=title,
        url=url,
        cat_name="书籍资料" if cat == 84 else "工具合集"
    )
    
    try:
        cursor.execute("""
            INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, 
            post_excerpt, post_status, comment_status, ping_status, post_name, to_ping, pinged, 
            post_modified, post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, 
            post_type, post_mime_type, comment_count)
            VALUES (1, NOW(), UTC_TIMESTAMP(), %s, %s, '', 'publish', 'closed', 'closed', %s, 
            '', '', NOW(), UTC_TIMESTAMP(), '', 0, %s, 0, 'post', '', 0)
        """, (content_html, title, slug, "https://skillxm.cn/?p=0"))
        
        post_id = cursor.lastrowid
        cursor.execute("UPDATE wp_posts SET guid='https://skillxm.cn/?p={}' WHERE ID={}".format(post_id, post_id))
        cursor.execute("INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES ({}, {}, 0)".format(post_id, cat))
        cursor.execute("UPDATE wp_term_taxonomy SET count = count + 1 WHERE term_taxonomy_id = {}".format(cat))
        
        conn.commit()
        print("[{}/{}] OK ID:{}".format(i+1, len(to_publish), post_id), flush=True)
        time.sleep(0.5)
    except Exception as e:
        conn.rollback()
        print("[{}/{}] FAIL: {} - {}".format(i+1, len(to_publish), title, e), flush=True)

conn.close()
print("\nDone!", flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/publish_missing.py', 'w') as f:
    f.write(publish_script)
sftp.close()

print("Script uploaded. Executing...", flush=True)

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 publish_missing.py", timeout=300)
output = stdout.read().decode('utf-8', errors='replace')
print(output, flush=True)

err = stderr.read().decode('utf-8', errors='replace')
if err:
    print("STDERR:", err, flush=True)

ssh.close()
