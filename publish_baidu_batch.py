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

resources = [
    # Education (84)
    {"title": "12个月从0赚到100万美金", "url": "https://pan.baidu.com/s/1irl6ngoJPEeMjoCQrBEkgA?pwd=24d2", "pwd": "24d2", "cat": 84},
    {"title": "百万富翁快车道", "url": "https://pan.baidu.com/s/1JAHYYJ2z0TVAXxeWPWaEUA?pwd=mc8r", "pwd": "mc8r", "cat": 84},
    {"title": "炒股养家传记新版", "url": "https://pan.baidu.com/s/13uAyoPifs2vI-BHL5L7O5g?pwd=4397", "pwd": "4397", "cat": 84},
    {"title": "Solidworks新手练习教程", "url": "https://pan.baidu.com/s/1QPPwZ87Vd7XJcoAAtY32YA?pwd=n77n", "pwd": "n77n", "cat": 84},
    {"title": "PPT简历模板免费下载", "url": "https://pan.baidu.com/s/18uSBrfYeRJLAqjncYlUUYw?pwd=1234", "pwd": "1234", "cat": 84},
    {"title": "超级个体 普通人创造财富的无限游戏", "url": "https://pan.baidu.com/s/1qf3PRuEd8B7lNUprOztwyQ?pwd=1234", "pwd": "1234", "cat": 84},
    {"title": "新手入行互联网月入6000完全指南", "url": "https://pan.baidu.com/s/1BWa_zHOAlDH2695UZbIPgg?pwd=1234", "pwd": "1234", "cat": 84},
    {"title": "中医笔记", "url": "https://pan.baidu.com/s/1fRk2ImfY3W-E7akzWkFYxQ?pwd=1234", "pwd": "1234", "cat": 84},
    {"title": "变频空调维修技术资料 格力美的高级教程", "url": "https://pan.baidu.com/s/13fn_zLJgSkcV6phBeZA9Dg?pwd=1234", "pwd": "1234", "cat": 84},
    {"title": "小家电维修从入门到精通", "url": "https://pan.baidu.com/s/1PfhiIBk1jfbSh2L6GUjAtw?pwd=1234", "pwd": "1234", "cat": 84},
    {"title": "AI扣子Coze自动化工作流教程", "url": "https://pan.baidu.com/s/1K6auy23mhGe8Ab2J8St7ag?pwd=1234", "pwd": "1234", "cat": 84},
    # Self Media (83)
    {"title": "知乎小说项目详细教程", "url": "https://pan.baidu.com/s/1H-FtZZtDe9ByonoChH6JzA?pwd=9tk5", "pwd": "9tk5", "cat": 83},
    {"title": "小红书电商项目教程 0-1入门全盘玩法", "url": "https://pan.baidu.com/s/1MW9xHKjxCMVHV94Ghm1lIA?pwd=je38", "pwd": "je38", "cat": 83},
    {"title": "爆款电影解说教程 影视解说实操", "url": "https://pan.baidu.com/s/1edQS5ssNBN64NwozUzpN8g?pwd=1234", "pwd": "1234", "cat": 83},
    {"title": "闲鱼冷门跑步项目 keep代跑日入教程", "url": "https://pan.baidu.com/s/1nm32PbjqybgSh-fEb4Mguw?pwd=1234", "pwd": "1234", "cat": 83},
    {"title": "爆款自媒体起号训练营 14天落地实操", "url": "https://pan.baidu.com/s/1Q_6UUhM8qG8Iud7DYY9svQ?pwd=1234", "pwd": "1234", "cat": 83},
    {"title": "AI图文带货实操课 新手从0-1", "url": "https://pan.baidu.com/s/1vtmiXvBWCq9B37ckyZApUg?pwd=1234", "pwd": "1234", "cat": 83},
    {"title": "小红书店铺课程", "url": "https://pan.baidu.com/s/1qTRWL99KKV1OPYIELsdNWQ?pwd=1234", "pwd": "1234", "cat": 83},
    {"title": "微头条公众号小绿书精准引流男粉到私域", "url": "https://pan.baidu.com/s/1tsyTteNPY37fgOL53MzE6w?pwd=1234", "pwd": "1234", "cat": 83},
    # Movies/Novels (86)
    {"title": "电影窒恋4K", "url": "https://pan.baidu.com/s/1w_0I2QynscpT843Et7aQtw?pwd=1234", "pwd": "1234", "cat": 86},
    {"title": "小说资源合集", "url": "https://pan.baidu.com/s/1udMbrWZPYH-797id14cK6w?pwd=1234", "pwd": "1234", "cat": 86},
]

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
    pwd = res["pwd"]
    cat = res["cat"]
    ts = str(int(time.time()))
    slug = "bd-{}-{}".format(ts, hashlib.md5(title.encode()).hexdigest()[:4])
    cat_name = cat_names.get(cat, "其他")

    content_html = (
        '<p>资源名称：{title}</p>'
        '<p>资源类型：{cat_name}</p>'
        '<p>📁 网盘来源：百度网盘</p>'
        '<p>⭐ <strong>使用方法：</strong>复制链接 → 打开百度网盘APP或网页版 → 输入提取码 → 保存到自己的网盘即可使用</p>'
        '<p>下载链接：<a href="{url}" target="_blank" rel="noopener">{url}</a></p>'
        '<p>🔑 提取码：<strong>{pwd}</strong></p>'
    ).format(title=title, url=url, pwd=pwd, cat_name=cat_name)

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
with sftp.open('/root/scripts/publish_baidu.py', 'w') as f:
    f.write(publish_script)
sftp.close()

print("Publishing 21 Baidu resources...", flush=True)

stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 publish_baidu.py", timeout=120)
output = stdout.read().decode('utf-8', errors='replace')
print(output, flush=True)

ssh.close()
